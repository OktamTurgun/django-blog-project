from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testauthor', password='Password123!')
        self.category = Category.objects.create(name='Texnologiya')
        self.tag = Tag.objects.create(name='Python')

    def test_category_and_tag_slug_generation(self):
        self.assertEqual(self.category.slug, 'texnologiya')
        self.assertEqual(self.tag.slug, 'python')

    def test_post_creation_and_slug_uniqueness(self):
        post1 = Post.objects.create(
            title='Django Asoslari',
            author=self.user,
            content='Django haqida maqola',
            category=self.category,
        )
        self.assertEqual(post1.slug, 'django-asoslari')
        self.assertEqual(post1.status, 'pending')
        self.assertEqual(post1.views_count, 0)

        # Duplicate title slug test
        post2 = Post.objects.create(
            title='Django Asoslari',
            author=self.user,
            content='Boshqa maqola',
            category=self.category,
        )
        self.assertEqual(post2.slug, 'django-asoslari-1')


class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='AuthorPass123!')
        self.other_user = User.objects.create_user(username='reader', password='ReaderPass123!')
        self.category = Category.objects.create(name='Dasturlash')
        self.tag = Tag.objects.create(name='Web')

        # Approved post
        self.approved_post = Post.objects.create(
            title='Tasdiqlangan Maqola',
            author=self.author,
            content='Bu maqola tasdiqlangan va hamma ko\'radi.',
            category=self.category,
            status='approved',
            is_featured=True,
        )
        self.approved_post.tags.add(self.tag)

        # Pending post
        self.pending_post = Post.objects.create(
            title='Kutilayotgan Maqola',
            author=self.author,
            content='Bu maqola hali moderatsiyada.',
            category=self.category,
            status='pending',
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.approved_post.title)
        self.assertNotContains(response, self.pending_post.title)
        self.assertIn('featured_posts', response.context)
        self.assertIn('latest_posts', response.context)
        self.assertIn('most_viewed', response.context)
        self.assertIn('weekly_popular', response.context)
        self.assertIn('monthly_popular', response.context)

    def test_post_list_view_only_shows_approved(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.approved_post.title)
        self.assertNotContains(response, self.pending_post.title)

    def test_post_list_category_filter_and_search(self):
        # Category filter
        response = self.client.get(reverse('post_list') + f'?category={self.category.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.approved_post.title)

        # Search query
        response = self.client.get(reverse('post_list') + '?q=Tasdiqlangan')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.approved_post.title)

        response = self.client.get(reverse('post_list') + '?q=MavjudEmasSoz')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.approved_post.title)

    def test_post_detail_view_increments_views(self):
        initial_views = self.approved_post.views_count
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.approved_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.approved_post.refresh_from_db()
        self.assertEqual(self.approved_post.views_count, initial_views + 1)

    def test_pending_post_access_permissions(self):
        # Anonymous user cannot view pending post
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.pending_post.slug}))
        self.assertEqual(response.status_code, 404)

        # Other non-staff user cannot view pending post
        self.client.login(username='reader', password='ReaderPass123!')
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.pending_post.slug}))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        # Author CAN view their pending post
        self.client.login(username='author', password='AuthorPass123!')
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.pending_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kutilayotgan Maqola')

    def test_post_create_view(self):
        # Anonymous redirect
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)

        # Authenticated create
        self.client.login(username='author', password='AuthorPass123!')
        response = self.client.post(reverse('post_create'), {
            'title': 'Yangi Muallif Posti',
            'content': 'Postning to\'liq matni',
            'category': self.category.id,
            'tags': [self.tag.id],
        })
        self.assertEqual(response.status_code, 302)

        created_post = Post.objects.get(title='Yangi Muallif Posti')
        self.assertEqual(created_post.author, self.author)
        self.assertEqual(created_post.status, 'pending')

    def test_comment_submission(self):
        # Anonymous cannot submit comment
        response = self.client.post(reverse('post_detail', kwargs={'slug': self.approved_post.slug}), {
            'content': 'Ajoyib maqola!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

        # Authenticated user submits comment
        self.client.login(username='reader', password='ReaderPass123!')
        response = self.client.post(reverse('post_detail', kwargs={'slug': self.approved_post.slug}), {
            'content': 'Ajoyib maqola!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.author, self.other_user)
        self.assertEqual(comment.post, self.approved_post)

    def test_comment_submission_does_not_increase_views(self):
        # 1. User visits post (GET)
        self.client.login(username='reader', password='ReaderPass123!')
        self.client.get(reverse('post_detail', kwargs={'slug': self.approved_post.slug}))
        self.approved_post.refresh_from_db()
        views_after_first_visit = self.approved_post.views_count

        # 2. User submits a comment (POST) with follow=True to follow the redirect
        self.client.post(
            reverse('post_detail', kwargs={'slug': self.approved_post.slug}),
            {'content': 'Yana bir fikr!'},
            follow=True
        )
        self.approved_post.refresh_from_db()
        # views_count must NOT have increased
        self.assertEqual(self.approved_post.views_count, views_after_first_visit)

    def test_repeated_page_refresh_does_not_increase_views(self):
        self.client.get(reverse('post_detail', kwargs={'slug': self.approved_post.slug}))
        self.approved_post.refresh_from_db()
        views_first = self.approved_post.views_count

        # Second GET in same session
        self.client.get(reverse('post_detail', kwargs={'slug': self.approved_post.slug}))
        self.approved_post.refresh_from_db()
        self.assertEqual(self.approved_post.views_count, views_first)

    def test_post_recommend_toggle(self):
        self.client.login(username='reader', password='ReaderPass123!')
        url = reverse('post_recommend', kwargs={'slug': self.approved_post.slug})

        # Add recommendation
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.approved_post.refresh_from_db()
        self.assertEqual(self.approved_post.recommendations_count, 1)

        # Toggle (remove recommendation)
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.approved_post.refresh_from_db()
        self.assertEqual(self.approved_post.recommendations_count, 0)

    def test_author_cannot_recommend_own_post(self):
        self.client.login(username='author', password='AuthorPass123!')
        url = reverse('post_recommend', kwargs={'slug': self.approved_post.slug})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.approved_post.refresh_from_db()
        self.assertEqual(self.approved_post.recommendations_count, 0)


class PostEditDeleteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='editauthor', password='AuthPass123!')
        self.other = User.objects.create_user(username='editother', password='OtherPass123!')
        self.post = Post.objects.create(
            title='Tahrirlash Testi',
            author=self.author,
            content='Test matni',
            status='approved',
        )

    def test_author_can_access_edit_page(self):
        self.client.login(username='editauthor', password='AuthPass123!')
        response = self.client.get(reverse('post_edit', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit(self):
        """Boshqa foydalanuvchi tahrirlash sahifasiga kira olmaydi."""
        self.client.login(username='editother', password='OtherPass123!')
        response = self.client.get(reverse('post_edit', kwargs={'slug': self.post.slug}), follow=True)
        self.assertEqual(response.status_code, 200)
        # Post o'zgarmasligi kerak
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Tahrirlash Testi')

    def test_edit_post_sets_status_to_pending(self):
        """Tahrirlanganda post status 'pending' ga qaytishi kerak."""
        self.client.login(username='editauthor', password='AuthPass123!')
        response = self.client.post(reverse('post_edit', kwargs={'slug': self.post.slug}), {
            'title': 'Yangilangan Sarlavha',
            'content': 'Yangilangan matn',
            'tags': [],
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.status, 'pending')
        self.assertEqual(self.post.title, 'Yangilangan Sarlavha')

    def test_author_can_delete_post(self):
        """Muallif o'z postini o'chira oladi."""
        self.client.login(username='editauthor', password='AuthPass123!')
        post_slug = self.post.slug
        response = self.client.post(reverse('post_delete', kwargs={'slug': post_slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(slug=post_slug).exists())

    def test_other_user_cannot_delete(self):
        """Boshqa foydalanuvchi postni o'chira olmaydi."""
        self.client.login(username='editother', password='OtherPass123!')
        self.client.post(reverse('post_delete', kwargs={'slug': self.post.slug}))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
