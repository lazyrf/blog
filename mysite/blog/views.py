from django.shortcuts import render, get_object_or_404
from django.http import Http404
from blog.models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    # Retrieve the object that matches the given parameters or and Http404 exceptioon if no object is found
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No post found.")

    return render(request, 'blog/post/detail.html', {'post': post})
