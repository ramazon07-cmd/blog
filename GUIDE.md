# Writespark Project Guide

## What This Project Is
Writespark is a Django-based blog platform focused on the writing experience. It provides post management, authentication, categories, comments with threads and likes, search, and a writers directory.

## Core Business Outcome
Help writers and content creators publish articles consistently with a clean, distraction-free interface that puts content first.

## Who It Is For
- Personal brands and writers
- Small business websites
- Content creators and bloggers
- Coaches/consultants who need a simple CMS-like blog

## Main Features

### Content Management
- Post model with draft/published status
- Auto-generated slugs from titles (with collision handling)
- Featured posts highlighting
- Category system with slug-based URLs
- Comma-separated tags for organization
- Auto-calculated read time (200 wpm from word count)
- Cover image upload support

### User & Authentication
- User registration and login flow
- Author-only edit/delete permissions (UserPassesTestMixin)
- UserProfile with avatar, role, and bio
- User dashboard showing drafts/published counts

### Engagement
- Reader comments on posts
- Nested comment replies (parent-child)
- Comment likes counter
- Rate-limited commenting (5/min per user)

### Discovery
- Post listing with pagination (9 per page)
- Search across title, subtitle, and content
- Category-based filtering
- Writers directory with post counts
- Home page with featured + recent posts

## Technical Architecture

### Models
- **Post**: title, slug, author, content, subtitle, image, category, is_featured, read_time, tags, status, timestamps
- **Category**: name, slug, description, created_at
- **Comment**: post, user, content, parent (self-ref), likes, created_at
- **UserProfile**: user, avatar, role, bio

### Views (CBVs + FBV)
- HomeView: Featured + recent posts
- PostListView: All published with search/filter
- PostDetailView: Single post with comments
- PostCreateView: LoginRequired
- PostUpdateView: LoginRequired + author-only
- PostDeleteView: LoginRequired + author-only
- UserDashboardView: Author's posts
- WritersView: All writers with post counts
- CategoryPostsView: Category-filtered posts
- SearchView: Full-text search
- RegisterView: User registration
- add_comment: Rate-limited comment creation

### URL Structure
- `/` — Home
- `/posts/` — Post list
- `/writers/` — Writers directory
- `/dashboard/` — Author dashboard
- `/post/new/` — Create post
- `/post/<slug>/` — Post detail
- `/post/<slug>/edit/` — Edit post
- `/post/<slug>/delete/` — Delete post
- `/post/<slug>/comment/` — Add comment
- `/category/<slug>/` — Category posts
- `/search/` — Search
- `/register/` — Register

### Key Implementation Details
- Slug auto-generation with increment suffix for collisions
- read_time auto-calculated from word count on save
- Author-only access enforced via UserPassesTestMixin
- Rate limiting on comments via django-ratelimit
- Database indexes on frequently queried fields

## Offer Positioning
"I help writers and content creators publish consistently using a custom Django blog platform with clean URLs, categories, threaded comments, and role-aware permissions."

## Suggested Pricing
- Basic setup and customization: $300 - $800
- Branded production-ready build: $800 - $1,200
- Ongoing maintenance/content support: $50 - $250/month

## High-ROI Next Upgrades
- Rich text editor and media embedding
- SEO metadata (meta descriptions, Open Graph tags)
- Comment moderation and anti-spam protection
- Analytics integration for content performance tracking
- Newsletter/email subscription integration
- Social sharing buttons