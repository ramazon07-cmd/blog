# Draftly

A lightweight, custom blog platform built for simplicity and speed.

## Problem

Writing and publishing blog content is painful without the right platform. Existing solutions are either bloated with features you don't need, locked into proprietary ecosystems, or require significant configuration before you can write a single word.

## Solution

Draftly is a minimal, custom blog platform designed around the writing experience. Built with Django, it strips away the complexity and delivers a clean, fast interface where content is the focus.

## Features

- **Full CRUD for Posts** — Create, read, update, and delete articles with a streamlined editor
- **Authentication System** — Register, login, and logout with secure session management
- **Image Upload** — Add cover images to posts with full media pipeline support
- **Slug-Based URLs** — Clean, readable URLs for every post (e.g., `/post/my-post-title`)
- **Search** — Find posts by title or content via keyword search
- **Comments** — Readers can engage with posts through comments (rate-limited to prevent spam)
- **Responsive Design** — Dark theme UI optimized for reading and writing on any device

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Django 5.2 |
| Database | SQLite |
| Auth | Django's built-in authentication |
| Media Storage | Django media files (local) |
| Frontend | HTML + Tailwind CSS |
| Rate Limiting | django-ratelimit |
| Config | python-dotenv |
| Image Processing | Pillow |

## Quick Start

```bash
# Clone and enter directory
cd draftly

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
draftly/
├── blog/                  # Main application
│   ├── models.py         # Post and Comment models
│   ├── views.py          # CBVs for CRUD + comment handler
│   ├── forms.py          # Post creation/editing forms
│   └── urls.py           # App routing
├── blog_project/         # Django project config
│   ├── settings.py       # Settings (DEBUG, ALLOWED_HOSTS, etc.)
│   └── urls.py           # Root URL configuration
├── templates/            # Global templates
│   ├── base.html         # Base layout with Tailwind dark theme
│   ├── blog/             # Post-related templates
│   └── registration/     # Auth templates
├── static/               # CSS, JS, and static assets
├── media/                # User-uploaded images
└── manage.py             # Django CLI
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable debug mode |
| `DJANGO_SECRET_KEY` | (insecure default) | Django secret key |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed HTTP hosts |

> **Note:** Set `DJANGO_SECRET_KEY` to a secure random value before deploying.
