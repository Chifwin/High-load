from django.http import HttpResponse, response
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .serializers import PostSerializer
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


# Create your views here.
def hello_view(request):
    return HttpResponse("Hello, Blog!")


def post_list(request: HttpResponse):
    paginator = Paginator(Post.objects.order_by("-created_at").all(), 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts_list.html', {"page_obj": page_obj})


def post_one(request: HttpResponse, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if not form.is_valid():
            return response.HttpResponseBadRequest()
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return render(request, 'post_one.html', {'post': post, 'form': CommentForm(), 'comments': Comment.objects.filter(post__pk=post_id)})


@login_required
def post_new(request: HttpResponse):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog-post-one', post_id=post.id)
        return response.HttpResponseBadRequest()
    return render(request, 'post_edit.html', {'form': PostForm()})


def illegal_post_mod(request: HttpResponse):
    return render(request, 'post_modified.html',
                  {'error': 'You are not allowed to modify the post as you are not creator of it!'})


@login_required
def post_edit(request: HttpResponse, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return illegal_post_mod(request)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog-post-one', post_id=post.id)
        return response.HttpResponseBadRequest()
    return render(request, 'post_edit.html', {'form': PostForm(instance=post)})


@login_required
def post_delete(request: HttpResponse, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return illegal_post_mod(request)
    else:
        title = post.title
        try:
            post.delete()
        except e:
            error = str(e)
        else:
            error = None
    return render(request, 'post_modified.html', {'title': title, 'error': error})
