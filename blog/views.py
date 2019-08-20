from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post, Category, Comment
from blog.forms import CommentForm

# def blog_index(request):
#     # The minus sign tells Django to start with the largest value rather than the smallest.
#     posts = Post.objects.all().order_by('-created_on')
#     context = {
#         "posts": posts,
#     }
#     return render(request, "blog/blog_index.html", context)

class BlogIndexView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/blog_index.html'

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog/blog_category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog/post_detail.html", context)