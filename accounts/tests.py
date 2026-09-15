from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile


class UserProfileModelTests(TestCase):
    def test_profile_auto_created_on_user_save(self):
        """User yaratilganda UserProfile avtomatik yaratilishi kerak."""
        user = User.objects.create_user(username='newuser', password='Test1234!')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.user, user)

    def test_profile_str(self):
        user = User.objects.create_user(username='struser', password='Test1234!')
        self.assertIn('struser', str(user.profile))

    def test_get_avatar_url_without_avatar(self):
        user = User.objects.create_user(username='noavatar', password='Test1234!')
        self.assertIsNone(user.profile.get_avatar_url())

    def test_total_views_and_recommendations_initially_zero(self):
        user = User.objects.create_user(username='zerouser', password='Test1234!')
        self.assertEqual(user.profile.total_views, 0)
        self.assertEqual(user.profile.total_recommendations, 0)


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='profileuser', password='Test1234!')
        self.other = User.objects.create_user(username='otheruser', password='Test1234!')

    def test_public_profile_page_accessible_by_anyone(self):
        """Istalgan foydalanuvchi profilni ko'ra olishi kerak."""
        response = self.client.get(reverse('profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'profileuser')

    def test_profile_edit_requires_login(self):
        """Login qilmagan foydalanuvchi tahrirlash sahifasiga kira olmasligi kerak."""
        response = self.client.get(reverse('profile_edit'))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_edit_works_for_authenticated_user(self):
        """Login qilgan foydalanuvchi o'z profilini tahrirlashi mumkin."""
        self.client.login(username='profileuser', password='Test1234!')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_save_bio(self):
        """Bio saqlash ishlashi kerak."""
        self.client.login(username='profileuser', password='Test1234!')
        response = self.client.post(reverse('profile_edit'), {
            'bio': 'Salom, men dasturchi',
            'website': '',
            'email': 'test@example.com',
            'first_name': '',
            'last_name': '',
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Salom, men dasturchi')

    def test_404_for_nonexistent_user_profile(self):
        """Mavjud bo'lmagan foydalanuvchi profili 404 qaytarishi kerak."""
        response = self.client.get(reverse('profile', kwargs={'username': 'nobody_xxxx'}))
        self.assertEqual(response.status_code, 404)
