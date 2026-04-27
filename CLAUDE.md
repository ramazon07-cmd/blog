# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Writespark is a Django-based blog platform focused on the writing experience. Built with Django 5.2, it features a clean dark-theme UI, category organization, threaded comments with likes, and role-aware permissions.

## Development Commands

```bash
# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create migrations (after model changes)
python manage.py makemigrations

# Create superuser (for admin access)
python manage.py createsuperuser

# Run tests
python manage.py test

# Run single test file
python manage.py test blog.tests

# Django shell
python manage.py shell
```

## Architecture & Structure

### High-Level Structure
```
writespark/
├── blog/                  # Main application
│   ├── models.py          # Post, Comment, Category, UserProfile
│   ├── views.py           # CBVs for CRUD + specialized views
│   ├── forms.py          # PostCreateForm, PostUpdateForm
│   ├── urls.py           # App routing (namespace: blog)
│   ├── admin.py          # Custom admin with inlines
│   └── templatetags/      # blog_extras.py with custom filters
├── blog_project/          # Django project config
│   ├── settings.py       # Settings (DB, static, security)
│   └── urls.py           # Root URL configuration
├── templates/             # Global templates
├── static/               # CSS, JS, and static assets
├── media/                # User-uploaded images
└── manage.py             # Django CLI
```

### Application Logic

**Models (`blog/models.py`):**
- `Category`: name, slug (auto), description, created_at
- `Post`: title, slug (auto with collision handling), author, content, subtitle, image, category, is_featured, read_time (auto), tags, status, timestamps
- `UserProfile`: user (OneToOne), avatar, role, bio
- `Comment`: post, user, content, parent (self-ref), likes, created_at

**Views (`blog/views.py`):**
- Class-Based Views (CBVs): HomeView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserDashboardView, WritersView, CategoryPostsView, SearchView, RegisterView
- Function-Based View (FBV): add_comment (rate-limited)

**URLs (`blog/urls.py`):**
- App name: `blog`
- Key routes: `/`, `/posts/`, `/writers/`, `/dashboard/`, `/post/new/`, `/post/<slug>/`, `/post/<slug>/edit/`, `/post/<slug>/delete/`, `/category/<slug>/`, `/search/`, `/register/`

**Forms (`blog/forms.py`):**
- `PostCreateForm`: title, subtitle, content, image, category, is_featured, tags
- `PostUpdateForm`: adds status field to PostCreateForm fields

## Key Implementation Details

### Post Slugification
- `Post.save()` auto-generates slug from title using `slugify()`
- Handles collisions by appending incrementing counter (`my-title-2`, `my-title-3`)
- Uses `exclude(pk=self.pk)` to allow self-update without false collision

### Read Time Calculation
- `Post.save()` calculates `read_time` from word count: `max(1, words // 200)`

### Access Control
- `PostUpdateView` and `PostDeleteView` use `UserPassesTestMixin` with `test_func()` checking `request.user == post.author`
- `PostCreateView` uses `LoginRequiredMixin`

### Content Visibility
- `PostListView` filters for `status='published'` posts
- Search via `q` GET parameter filters title, subtitle, content
- Category filtering via `category` GET parameter

### Commenting
- `add_comment` view rate-limited to 5/min per user via `django-ratelimit`
- Comments linked to Post and User
- Nested replies via self-referential `parent` field

### Database Indexes
- Composite indexes: (status, -created_at), (author, -created_at), (category, -created_at), (is_featured, -created_at)
- Single field indexes: slug, author, category, is_featured, created_at

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable debug mode |
| `DJANGO_SECRET_KEY` | (insecure default) | Django secret key |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed HTTP hosts |
| `DATABASE_URL` | (not set) | Neon PostgreSQL connection string |