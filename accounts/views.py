from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, ProfileEditForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def profile_view(request, username):
    """Ommaviy profil sahifasi — istalgan foydalanuvchi ko'ra oladi."""
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.filter(status='approved').select_related('category').prefetch_related('tags')

    context = {
        'profile_user': profile_user,
        'posts': posts,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Foydalanuvchi faqat o'z profilini tahrirlaydi."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})
