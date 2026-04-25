from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Post, Comment, Category, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'avatar']
    search_fields = ['user__username', 'role']
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Profile Info', {'fields': ('avatar', 'role', 'bio')}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'read_time', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'subtitle']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('title',)}),
        ('Content', {'fields': ('subtitle', 'content', 'image')}),
        ('Metadata', {'fields': ('category', 'tags', 'is_featured', 'read_time', 'status')}),
        ('Author & Timestamps', {'fields': ('author', ('created_at', 'updated_at'))}),
    )
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content_preview', 'likes', 'parent', 'created_at']
    list_filter = ['created_at', 'parent']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {'fields': ('post', 'user', 'content')}),
        ('Engagement', {'fields': ('likes', 'parent')}),
        ('Metadata', {'fields': ('created_at',)}),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


# Extend the existing User Admin with inline profile and posts
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ['title', 'status', 'is_featured', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True
    show_change_link = True


# Unregister the default UserAdmin and re-register with our inlines
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, PostInline]
