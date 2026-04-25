from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()


@register.filter
def time_ago(value):
    """Returns human-readable 'time ago' string like '2 hours ago', '3 days ago'"""
    if not value:
        return ''
    now = timezone.now()
    diff = now - value
    if diff.total_seconds() < 60:
        return 'just now'
    return f'{timesince(value)} ago'


@register.filter
def reading_time(post):
    """Calculates reading time from word count (200 words per minute)"""
    if not post:
        return 1
    content = getattr(post, 'content', '') or ''
    words = len(content.split())
    return max(1, words // 200)


@register.filter
def tag_list(tags_string):
    """Splits comma-separated tags into a list"""
    if not tags_string:
        return []
    return [tag.strip() for tag in tags_string.split(',') if tag.strip()]


@register.filter
def category_name(category):
    """Returns category name or uppercase default"""
    if category:
        return category.name.upper()
    return 'ARTICLE'
