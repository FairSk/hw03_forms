from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect


from .forms import PostForm
from .models import Group, Post, User


def pager(request, post_list):
    return Paginator(post_list, 10).get_page(request.GET.get('page'))


def index(request):
    post_list = Post.objects.all()
    return render(request, 'posts/index.html', {
        'page_obj': pager(request, post_list)
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    return render(request, 'posts/group_list.html', {
        'group': group,
        'page_obj': pager(request, group.posts.all())
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    return render(request, 'posts/profile.html',
                  {'page_obj': pager(request, author.posts.all()),
                   'author': author})


def post_detail(request, post_id):
    exact_post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {
        'post': exact_post
    })


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, template, {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    return render(request, 'posts/post_create.html',
                  {'is_edit': True, 'form': form})
