from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import POSTS_PER_PAGE
from blog.models import Category, Post


def get_posts_queryset():
    """Возвращает базовый QuerySet для опубликованных постов."""
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).select_related('category', 'author', 'location')


def index(request):
    """Главная страница - выводит пять последних опубликованных постов."""
    post_list = get_posts_queryset().order_by('-pub_date')[:POSTS_PER_PAGE]

    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Детальная страница поста с проверкой всех условий."""
    post = get_object_or_404(
        get_posts_queryset(),
        pk=post_id
    )

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница с постами определенной категории."""
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
            slug=category_slug
        )
    )

    post_list = get_posts_queryset().filter(
        category=category
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
