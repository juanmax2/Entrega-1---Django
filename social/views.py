from django.shortcuts import render

from profiles.models import UserProfile, Follow
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, ProfileFollow
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormView
from contact.forms import ContactForm
from contact.models import ContactMessage
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        last_posts = Post.objects.none()
        
        if user.is_authenticated:
            other_users = User.objects.exclude(id=user.id)
            last_posts = Post.objects.filter(user__in=other_users).order_by('-created_at')
        
        else:
            last_posts = Post.objects.all().order_by('-created_at')[:9]
        
        context['last_posts'] = last_posts
        
        return context
    

class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    
    def form_valid(self, form):
        user = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=user, password=password)
        
        if user is not None:
            
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Welcome, {user.username}")
            
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(self.request, messages.ERROR, "Usuario o contraseña incorrecto")
            return super(LoginView, self).form_invalid(form)
        
class RegisterView(CreateView):
    template_name = 'core/register.html'
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

class LegalView(TemplateView):
    template_name = 'core/legal.html'
  
  
class ContactView(CreateView):
        model = ContactMessage
        template_name = 'core/contact.html'
        form_class = ContactForm
        success_url = reverse_lazy('contact')

        def form_valid(self, form):
            messages.success(self.request, "¡Gracias por contactar con Social Music! Te responderemos pronto.")
            return super().form_valid(form)
    
  
@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView, FormView):
    template_name = 'core/profile_detail.html'  
    model = UserProfile
    context_object_name = 'profile'
    form_class = ProfileFollow
    
    def form_valid(self, form):
        profile_pk = form.cleaned_data.get('profile_pk')
        action = form.cleaned_data.get('action')
        profile = UserProfile.objects.get(pk=profile_pk)
        self.request.user.profile.follow(profile)
        
        if action == 'follow':
            Follow.objects.get_or_create(
                follower=self.request.user.profile,
                following=profile
            )
        elif action == 'unfollow':
            Follow.objects.filter(
                follower=self.request.user.profile,
                following=profile
            ).delete()
            
        return HttpResponseRedirect(reverse('profile_detail', args=[profile_pk]))
        
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        
        following = Follow.objects.filter(
            follower=self.request.user.profile,
            following=self.get_object()
        ).exists()
        
        context['following'] = following
        return context
    
    
    
@method_decorator(login_required, name='dispatch') 
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'core/profile_update.html'
    context_object_name = 'profile'
    form_class = ProfileUpdateForm
    
    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Perfil editado correctamente.')
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])
    
    
        
  
@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado la sesión correctamente.")
    return HttpResponseRedirect(reverse('home'))


