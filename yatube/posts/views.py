from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Group, Post, User


def pager(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    context = {
        'page_obj': pager(request, post_list)}
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
        'page_obj': pager(request, posts),
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    user_post_list = author.posts.all()
    context = {
        'page_obj': pager(request, user_post_list),
        'author': author,
        'user_post_list': user_post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    exact_post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, id=exact_post.author.id)
    post_list = author.posts.all()
    context = {
        'post': exact_post,
        'post_list': post_list}
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    form = form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, template, {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    username = str(request.user)
    return redirect('posts:profile', username)


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    context = {
        'is_edit': True,
        'form': form}
    return render(request, template, context)
