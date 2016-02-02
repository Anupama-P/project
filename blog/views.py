from blog.models import Blog
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect
from django.template import RequestContext
from django.views.generic.edit import UpdateView


def index(request):

    return render(request, 'blog/index.html', {
        'posts': Blog.objects.all()
    })


def post_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('index')

    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_remove(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('index')


def post_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
