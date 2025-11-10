from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def index(request):
    """Главная страница - выводит пять последних опубликованных постов."""
    template = 'blog/index.html'

    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).select_related(
        'category', 'author', 'location'
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Детальная страница поста с проверкой всех условий."""
    template = 'blog/detail.html'

    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            pk=post_id
        ).select_related('category', 'author', 'location')
    )

    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Страница с постами определенной категории."""
    template = 'blog/category.html'

    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
            slug=category_slug
        )
    )

    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related(
        'category', 'author', 'location'
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
