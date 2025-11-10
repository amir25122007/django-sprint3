from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.utils import timezone
from .models import Post, Category, Location


def index(request):
    """
    Главная страница - выводит пять последних опубликованных постов
    """
    template = 'blog/index.html'

    # Получаем только опубликованные посты с учетом всех условий
    post_list = Post.objects.filter(
        is_published=True,  # Пост опубликован
        category__is_published=True,  # Категория опубликована
        pub_date__lte=timezone.now()  # Дата публикации не позже текущего времени
    ).select_related(
        'category', 'author', 'location'
    ).order_by('-pub_date')[:5]  # Последние 5 постов

    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """
    Детальная страница поста с проверкой всех условий
    """
    template = 'blog/detail.html'

    # Получаем пост или 404 ошибку с проверкой всех условий
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,  # Пост опубликован
            category__is_published=True,  # Категория опубликована
            pub_date__lte=timezone.now(),  # Дата публикации не позже текущего времени
            pk=post_id
        ).select_related('category', 'author', 'location')
    )

    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """
    Страница с постами определенной категории
    """
    template = 'blog/category.html'

    # Получаем категорию или 404 ошибку
    # Если категория не опубликована - вернет 404
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,  # Категория должна быть опубликована
            slug=category_slug
        )
    )

    # Получаем опубликованные посты этой категории
    post_list = Post.objects.filter(
        category=category,
        is_published=True,  # Пост опубликован
        pub_date__lte=timezone.now()  # Дата публикации не позже текущего времени
    ).select_related(
        'category', 'author', 'location'
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)