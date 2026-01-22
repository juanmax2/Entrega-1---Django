from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from post.models import Post
from .forms import PostCreateForm, CommentCreateForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'posts/post_create.html'
    model = Post
    form_class = PostCreateForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Publicación creada correctamente')
        
        return super(PostCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('home')
    

@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView, CreateView):
    template_name = 'posts/post_detail.html'
    model = Post
    context_object_name = 'post'
    form_class = CommentCreateForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', args=[self.get_object().pk])
    

@login_required
def post_like_ajax(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse(
            {
                'liked' : liked,
                'count' : post.likes.count()      
        })