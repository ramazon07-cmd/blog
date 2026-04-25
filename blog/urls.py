from django.urls import path
from .views import (
    HomeView, PostListView, PostDetailView, PostCreateView, PostUpdateView,
    PostDeleteView, RegisterView, add_comment, CategoryPostsView, SearchView,
    UserDashboardView
)

app_name = 'blog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('category/<slug:slug>/', CategoryPostsView.as_view(), name='category_posts'),
    path('search/', SearchView.as_view(), name='search'),
    path('register/', RegisterView.as_view(), name='register'),
]
