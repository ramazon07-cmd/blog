import re
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.urls import reverse_lazy
from itertools import chain
from django.db.models import Q, Count
from django.contrib.auth.models import User
from .models import Post, Comment, Category
from .forms import PostCreateForm, PostUpdateForm


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = None

    def get_queryset(self):
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured posts — up to 3, newest first
        context['featured_posts'] = (
            Post.objects.filter(status='published', is_featured=True)
            .select_related('author', 'category')
            .order_by('-created_at')[:3]
        )

        # Recent non-featured posts — up to 6, newest first
        context['recent_posts'] = (
            Post.objects.filter(status='published', is_featured=False)
            .select_related('author', 'category')
            .order_by('-created_at')[:6]
        )

        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
 
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        category_slug = self.request.GET.get('category', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(subtitle__icontains=query)
            )
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.filter(status='published').select_related('author', 'category')
 
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_categories'] = Category.objects.all()
        ctx['query'] = self.request.GET.get('q', '')
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category').prefetch_related('comments')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = list(self.object.comments.order_by('-created_at'))
        ctx['all_categories'] = Category.objects.all()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'published'
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class UserDashboardView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by('-created_at').select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drafts_count'] = Post.objects.filter(author=self.request.user, status='draft').count()
        context['published_count'] = Post.objects.filter(author=self.request.user, status='published').count()
        return context


class WritersView(ListView):
    model = Post
    template_name = 'blog/writers.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['writers'] = User.objects.filter(
            blog_posts__status='published'
        ).annotate(
            post_count=Count('blog_posts')
        ).order_by('-post_count')
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            category=self.category,
            status='published'
        ).order_by('-created_at').select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['all_categories'] = Category.objects.all()
        return context


class SearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category_slug = self.request.GET.get('category', '')
        posts = Post.objects.filter(status='published')

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(subtitle__icontains=query)
            )
        if category_slug:
            posts = posts.filter(category__slug=category_slug)

        return posts.order_by('-created_at').select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['all_categories'] = Category.objects.all()
        return context


@login_required(login_url='login')
@ratelimit(key='user', rate='5/m', method='POST', block=True)
def add_comment(request, slug):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            messages.error(request, 'Comment cannot be empty.')
            return redirect('blog:post_list')

        try:
            post = Post.objects.get(slug=slug)
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, 'Comment posted!')
        except Post.DoesNotExist:
            messages.error(request, 'Post not found.')
            return redirect('blog:post_list')

        return redirect('blog:post_detail', slug=post.slug)

    return redirect('blog:post_list')
