from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Category, Post


def home_view(request):
    approved_posts = Post.objects.filter(status='approved').select_related('author', 'category').prefetch_related('tags', 'recommenders')

    # 1. Eng yangi postlar
    latest_posts = approved_posts.order_by('-created_at')[:5]

    # 2. Eng ko'p ko'rilgan postlar (umumiy)
    most_viewed = approved_posts.order_by('-views_count')[:5]

    # 3. Haftaning eng ommabop postlari (oxirgi 7 kun ichida)
    week_ago = timezone.now() - timedelta(days=7)
    weekly_popular = approved_posts.filter(
        created_at__gte=week_ago
    ).order_by('-views_count')[:5]

    # 4. Oyning eng ommabop postlari (oxirgi 30 kun ichida)
    month_ago = timezone.now() - timedelta(days=30)
    monthly_popular = approved_posts.filter(
        created_at__gte=month_ago
    ).order_by('-views_count')[:5]

    # 5. Tavsiya qilingan postlar (admin tanlagan yoki eng ko'p foydalanuvchi tavsiya qilganlar)
    featured_posts = approved_posts.annotate(
        recommends_count=Count('recommenders')
    ).filter(
        Q(is_featured=True) | Q(recommends_count__gt=0)
    ).order_by('-is_featured', '-recommends_count', '-created_at')[:5]

    context = {
        'latest_posts': latest_posts,
        'most_viewed': most_viewed,
        'weekly_popular': weekly_popular,
        'monthly_popular': monthly_popular,
        'featured_posts': featured_posts,
    }
    return render(request, 'blog/home.html', context)


def post_list_view(request):
    posts = Post.objects.filter(status='approved').select_related('author', 'category').prefetch_related('tags')

    selected_category = None
    category_slug = request.GET.get('category')
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=selected_category)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail_view(request, slug):
    post = get_object_or_404(Post.objects.select_related('author', 'category').prefetch_related('tags'), slug=slug)

    # Muallif yoki admin bo'lmagan foydalanuvchilar faqat tasdiqlangan postlarni ko'ra oladi
    if post.status != 'approved':
        if not request.user.is_authenticated or (post.author != request.user and not request.user.is_staff):
            raise Http404("Post mavjud emas yoki hali tasdiqlanmagan.")

    # Ko'rishlar sonini faqat GET so'rovida va sessiyada bir marta oshirish
    if request.method == 'GET':
        viewed_posts = request.session.get('viewed_posts', [])
        if post.id not in viewed_posts:
            post.views_count += 1
            post.save(update_fields=['views_count'])
            viewed_posts.append(post.id)
            request.session['viewed_posts'] = viewed_posts

    comments = post.comments.select_related('author').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Izoh qoldirish uchun tizimga kiring.")
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Izohingiz muvaffaqiyatli qo'shildi.")
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    user_has_recommended = False
    if request.user.is_authenticated:
        user_has_recommended = post.recommenders.filter(id=request.user.id).exists()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'user_has_recommended': user_has_recommended,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_recommend_view(request, slug):
    post = get_object_or_404(Post, slug=slug, status='approved')
    if request.method == 'POST':
        if post.author == request.user:
            messages.warning(request, "O'z postingizni o'zingiz tavsiya qila olmaysiz.")
        elif request.user in post.recommenders.all():
            post.recommenders.remove(request.user)
            messages.info(request, "Tavsiyangiz bekor qilindi.")
        else:
            post.recommenders.add(request.user)
            messages.success(request, f"'{post.title}' postini tavsiya qildingiz! Rahmat.")
    return redirect('post_detail', slug=post.slug)


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'pending'
            post.save()
            form.save_m2m()
            messages.success(request, "Postingiz yuborildi va admin tasdig'ini kutmoqda.")
            return redirect('my_posts')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user).select_related('category')
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def post_edit_view(request, slug):
    """Faqat muallif o'z postini tahrirlaydi. Tahrirlanganda status 'pending' ga qaytadi."""
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, "Siz faqat o'z postingizni tahrirlashingiz mumkin.")
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            # Tahrirlanganda qayta moderatsiyaga yuboriladi
            edited_post.status = 'pending'
            edited_post.save()
            form.save_m2m()
            messages.success(request, "Post yangilandi. Admin tomonidan qayta ko'rib chiqiladi.")
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'is_edit': True})


@login_required
def post_delete_view(request, slug):
    """Faqat muallif o'z postini o'chiradi."""
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, "Siz faqat o'z postingizni o'chirishingiz mumkin.")
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f"'{title}' nomli post o'chirildi.")
        return redirect('my_posts')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


