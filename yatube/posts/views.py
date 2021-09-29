from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


def paginator_my(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.all()
    page_obj = paginator_my(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginator_my(request, post_list)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    full_name = user.get_full_name()

    post_list = user.posts.all()
    post_count = post_list.count()
    page_obj = paginator_my(request, post_list)

    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'full_name': full_name,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, id=post.author.id)

    full_name = author.get_full_name()
    post_count = author.posts.all().count()
    context = {
        'post': post,
        'author': author,
        'full_name': full_name,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST) 
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.author = request.user
            form_obj.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    

    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.pk)
    is_edit = True

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) 
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.author = request.user
            form_obj.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'is_edit': is_edit,
    }

    
    return render(request, 'posts/create_post.html', context)
