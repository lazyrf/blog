from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.models import Post
from blog.forms import EmailPostForm


def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    # Get page object that includes page_number and posts
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # If page_nubmer is out of range
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    # Retrieve the object that matches the given parameters or and Http404 exceptioon if no object is found
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day)
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No post found.")

    return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrive post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # From fields pass validation
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post.share.html', {'post': post, 'form': form})
