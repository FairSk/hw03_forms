from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj}
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    user_post_list = Post.objects.filter(author=user.id)
    paginator = Paginator(user_post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': user_post_list,
        'page_obj': page_obj,
        'username': user}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    exact_post = Post.objects.get(id=post_id)
    post_list = Post.objects.filter(author=exact_post.author)
    context = {
        'post': exact_post,
        'post_list': post_list}
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
    else:
        form = PostForm()
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    post = Post.objects.get(id=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post.pk)
        context = {
            'is_edit': True,
            'form': form,
        }
        return render(request, template, context)
    else:
        return redirect('posts:post_detail', post_id)
