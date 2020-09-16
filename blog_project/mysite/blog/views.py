from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog import models
from blog import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.urls import reverse_lazy
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = models.Post
    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = models.Post
    #template_name = 'post_detail.html'

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    #redirect_field_name = 'blog/post_detail.html'
    form_class = forms.PostForm
    model = models.Post
    

class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = models.Post
    form_class = forms.PostForm

class DeletePostView(DeleteView):
    model = models.Post
    success_url = reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin,ListView):
    url = '/login/'
    redirect_field_name = 'blog:post_list'
    model = models.Post
    template_name = 'post_draft_list.html'

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull = True).order_by('-create_date')

@login_required
def post_publish(request,pk):
    post = get_object_or_404(models.Post,pk =pk)
    post.publish()
    return redirect('blog:post_detail',pk = post.pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form = forms.CommentForm()
    return render(request,'blog/comment_form.html',{'form':form}) #this seems wrong

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk = comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(models.Comment,pk = pk)
    saving_for_future_coz_later_will_be_deleted = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk = saving_for_future_coz_later_will_be_deleted)        





