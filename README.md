# Writespark

A lightweight blog platform built for writers and content creators.

## Problem

Writing and publishing content shouldn't require navigating complex CMS interfaces or wrestling with bloated platforms. Creators need a focused space where the writing experience comes first.

## Solution

Writespark is a minimal blog platform designed around the writing experience. Built with Django, it delivers a clean, fast interface where content is the focus — no bloat, no page builders slowing you down.

## Features

- **Full CRUD for Posts** — Create, read, update, and delete articles with a streamlined editor
- **Authentication System** — Register, login, and logout with secure session management
- **Author Dashboard** — Personal dashboard showing drafts and published post counts
- **Featured Posts** — Highlight important articles with is_featured flag
- **Category System** — Organize posts by topic with slug-based category pages
- **Slug-Based URLs** — Clean, readable URLs for every post (e.g., `/post/my-post-title`)
- **Auto-calculated Read Time** — Posts display estimated reading time (200 wpm)
- **Tags** — Comma-separated tags for post organization
- **Search** — Find posts by title, subtitle, or content via keyword search
- **Reader Comments** — Engage with readers through comments (rate-limited at 5/min)
- **Nested Replies** — Comment threads with parent-child relationships
- **Comment Likes** — Readers can like comments
- **Writers Directory** — Browse all published writers and their post counts
- **Responsive Design** — Dark theme UI optimized for reading and writing on any device

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Django 5.2 |
| Database | SQLite (local) / Neon PostgreSQL (production via DATABASE_URL) |
| Auth | Django's built-in authentication |
| Media Storage | Django media files (local) |
| Frontend | HTML + Tailwind CSS |
| Rate Limiting | django-ratelimit |
| Config | python-dotenv |
| Image Processing | Pillow |

## Quick Start

```bash
# Clone and enter directory
cd writespark

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to start.

## Project Structure

```
writespark/
├── blog/                  # Main application
│   ├── models.py          # Post, Comment, Category, UserProfile models
│   ├── views.py           # CBVs for CRUD + specialized views
│   ├── forms.py           # PostCreateForm, PostUpdateForm
│   ├── urls.py            # App routing (namespace: blog)
│   ├── admin.py           # Custom admin configuration
│   └── templatetags/      # Custom template filters
├── blog_project/          # Django project config
│   ├── settings.py        # Settings (DEBUG, ALLOWED_HOSTS, DB, etc.)
│   └── urls.py            # Root URL configuration
├── templates/             # Global templates
│   ├── base.html          # Base layout with Tailwind dark theme
│   ├── blog/              # Post-related templates
│   ├── components/        # Reusable components (navbar, footer)
│   └── registration/      # Auth templates
├── static/                # CSS, JS, and static assets
├── media/                 # User-uploaded images
└── manage.py             # Django CLI
```

## Core Models

### Post
- title, subtitle, content, slug (auto-generated)
- author (ForeignKey to User)
- category (ForeignKey to Category, optional)
- image (optional cover image)
- is_featured (boolean)
- read_time (auto-calculated from word count)
- tags (comma-separated string)
- status (draft/published)
- created_at, updated_at (auto timestamps)

### Category
- name, slug (auto-generated)
- description (optional)
- created_at (auto timestamp)

### Comment
- post (ForeignKey to Post)
- user (ForeignKey to User)
- content
- parent (self-referential ForeignKey for replies)
- likes (counter)
- created_at (auto timestamp)

### UserProfile
- user (OneToOne to User)
- avatar, role, bio

## URL Routes

| URL | View | Purpose |
|-----|------|---------|
| `/` | HomeView | Featured + recent posts |
| `/posts/` | PostListView | All published posts (paginated) |
| `/writers/` | WritersView | Writers directory |
| `/dashboard/` | UserDashboardView | Author's post management |
| `/post/new/` | PostCreateView | Create new post |
| `/post/<slug>/` | PostDetailView | Single post view |
| `/post/<slug>/edit/` | PostUpdateView | Edit existing post |
| `/post/<slug>/delete/` | PostDeleteView | Delete post |
| `/post/<slug>/comment/` | add_comment | Add comment (rate-limited) |
| `/category/<slug>/` | CategoryPostsView | Posts by category |
| `/search/` | SearchView | Search posts |
| `/register/` | RegisterView | User registration |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable debug mode |
| `DJANGO_SECRET_KEY` | (insecure default) | Django secret key |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed HTTP hosts |
| `DATABASE_URL` | (not set) | Neon PostgreSQL connection string |

> **Note:** Set `DJANGO_SECRET_KEY` to a secure random value before deploying.