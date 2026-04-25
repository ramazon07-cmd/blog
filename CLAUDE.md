# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands
- Run server: `python manage.py runserver`
- Apply migrations: `python manage.py migrate`
- Make migrations: `python manage.py makemigrations`
- Create superuser: `python manage.py createsuperuser`
- Run tests: `python manage.py test`
- Run a single test: `python manage.py test blog.tests` (assuming tests are in `blog/tests.py`)
- Create a shell: `python manage.py shell`

## Architecture & Structure
The project is a Django-based blog application.

### High-Level Structure
- `blog_project/`: Project configuration (settings, root URLs, WSGI/ASGI).
- `blog/`: Main application logic.
    - `models.py`: Defines `Post` (with slug generation and status) and `Comment`.
    - `views.py`: Uses a mix of Class-Based Views (CBVs) for CRUD operations and function-based views for specific actions like adding comments.
    - `urls.py`: Application-specific routing namespaced as `blog`.
    - `forms.py`: Contains forms for post creation/editing.
- `templates/`: Global templates, including a base layout and registration pages.
- `static/`: Global static assets (CSS, JS).

### Key Logic
- **Post Slugification**: `Post.save()` automatically generates a slug from the title if one isn't provided.
- **Access Control**: `PostUpdateView` and `PostDeleteView` use `UserPassesTestMixin` to ensure only the author can modify or delete their posts.
- **Content Visibility**: `PostListView` filters for `status='published'` posts and supports keyword search via the `q` GET parameter.
- **Commenting**: Comments are linked to both a `Post` and a `User`.
