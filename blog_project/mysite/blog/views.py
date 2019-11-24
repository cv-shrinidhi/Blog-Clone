from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from blog.models import Comment, Post
from django.urls import reverse_lazy

# Create your views here.

class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model = Post

    # querysets used to read data from database, filter it and order it
    def get_queryset(self):
        # running sql type query on model Post
        # grab the published dates which are less than or equal to current time and order them by published date
        # order_by('-published_date') orders in descending order, ie, recent blog post comes at the top
        # order_by('published_date') orders in ascending order
        # __lte is filter condition which specifies less than or equal to
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    # whichever object is sent to postdetailview will be automatically displayed in the form of detail view

# we dont want anyone to access createpostview so we import mixins
# it has the same purpose as decorators for authentication and authorization
# decorators with function based views and mixins with class based views
class CreatePostView(LoginRequiredMixin, CreateView):
    login_requried = '/login'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_requried = '/login'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


################################################################################################################


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST': # if the user has commented and clicked on post comment
        form = CommentForm(request.POST)
        if form.is_valid(): # if the entries in the comment form is valid
            comment = form.save(commit = False) # store it temporarily
            comment.post = post # associating the comment wala post to the actual post
            comment.save() #save it to the post
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')
