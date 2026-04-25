from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'content', 'image', 'category', 'is_featured', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 font-headline-lg text-headline-lg placeholder:text-zinc-700 text-on-surface resize-none h-auto',
                'placeholder': 'Untitled Story',
                'rows': 1
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 font-body-lg text-body-lg placeholder:text-zinc-600 text-on-surface-variant resize-none h-auto',
                'placeholder': 'Add a subtitle...',
                'rows': 1
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 font-body-lg text-body-lg placeholder:text-zinc-700 text-on-surface-variant leading-relaxed min-h-[400px] resize-none',
                'placeholder': 'Begin your masterpiece...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-surface-container-low border border-white/10 rounded-lg px-4 py-3 text-on-surface'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-white/20 bg-surface-container-low text-primary focus:ring-primary'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 text-sm text-on-surface-variant placeholder:text-zinc-600',
                'placeholder': 'Add tags (comma-separated)...'
            }),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'content', 'image', 'category', 'is_featured', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 font-headline-lg text-headline-lg placeholder:text-zinc-700 text-on-surface resize-none h-auto',
                'placeholder': 'Untitled Story',
                'rows': 1
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 font-body-lg text-body-lg placeholder:text-zinc-600 text-on-surface-variant resize-none h-auto',
                'placeholder': 'Add a subtitle...',
                'rows': 1
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 font-body-lg text-body-lg placeholder:text-zinc-700 text-on-surface-variant leading-relaxed min-h-[400px] resize-none',
                'placeholder': 'Begin your masterpiece...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-surface-container-low border border-white/10 rounded-lg px-4 py-3 text-on-surface'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 rounded border-white/20 bg-surface-container-low text-primary focus:ring-primary'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 text-sm text-on-surface-variant placeholder:text-zinc-600',
                'placeholder': 'Add tags (comma-separated)...'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full bg-surface-container-low border border-white/10 rounded-lg px-4 py-3 text-on-surface'
            }),
        }
