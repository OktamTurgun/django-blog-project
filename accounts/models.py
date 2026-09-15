from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500, help_text="O'zingiz haqida qisqacha ma'lumot (max 500 belgi)")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True, help_text="Shaxsiy veb-sayt yoki ijtimoiy tarmoq havolasi")

    def __str__(self):
        return f"{self.user.username} profili"

    def get_avatar_url(self):
        """Avatar URL ni qaytaradi, aks holda None qaytaradi."""
        if self.avatar:
            return self.avatar.url
        return None

    @property
    def total_views(self):
        """Foydalanuvchining barcha tasdiqlangan postlari umumiy ko'rishlari."""
        return self.user.posts.filter(status='approved').aggregate(
            total=models.Sum('views_count')
        )['total'] or 0

    @property
    def total_recommendations(self):
        """Foydalanuvchi postlariga yig'ilgan umumiy tavsiyalar soni."""
        from blog.models import Post
        count = 0
        for post in self.user.posts.filter(status='approved'):
            count += post.recommenders.count()
        return count


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """User yaratilganda avtomatik UserProfile yaratadi."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User saqlanganda unga tegishli profil ham saqlanadi."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
