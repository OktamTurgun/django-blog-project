from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'recommendations_count_display', 'views_count', 'created_at')
    list_filter = ('status', 'is_featured', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    actions = ['approve_posts', 'reject_posts']

    @admin.display(description="Tavsiyalar")
    def recommendations_count_display(self, obj):
        return obj.recommenders.count()


    @admin.action(description="Tanlangan postlarni tasdiqlash")
    def approve_posts(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Tanlangan postlarni rad etish")
    def reject_posts(self, request, queryset):
        queryset.update(status='rejected')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('content',)
