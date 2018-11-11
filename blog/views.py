from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (View, TemplateView, ListView, DetailView,
									CreateView, UpdateView, DeleteView)
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin # so can use decorator in a class based view
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone									


									
class AboutView(TemplateView):
    template_name = 'blog/about.html'
	
class PostListView(ListView):
    model = Post
	
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
# basically doing a query on model grab post model, grab published date then, lte= less than or equal tobytes
#then order them by newest blog post first i.e. descending place first, the dash does this

class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
	
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm

    model = Post	
	
class PostDeleteView(LoginRequiredMixin, DeleteView):
	
    model = Post

    success_url = reverse_lazy('post_list')	# maybe not need blog

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html' 
	
	
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')	 
# checking that the draft does not have a published date i'm guessing that if it does have a published date it is a legit post 		
 

######################################
######################################
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)  	



@login_required
def add_comment_to_post(request, pk):

    post = get_object_or_404(Post, pk=pk)
	
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post= post # see line 66
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk) # have to say comment.post because it is in a function where only comment is defined
	
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk # we are deleting this comment so need to grab the pk from the comment before deleting so we can use it in redirect
    comment.delete()
    return redirect('post_detail', pk=post_pk)	
	
     