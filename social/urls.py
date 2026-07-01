
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
from django.urls import re_path


from post.views import PostCreateView, PostDetailView, post_like_ajax
from .views import HomeView, LoginView, LegalView, ContactView, RegisterView, logout_view, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<pk>', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/detail/<pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/like_ajax/<pk>/', post_like_ajax, name = 'post_like_ajax'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('admin/', admin.site.urls),
    
]
if settings.DEBUG:
    # 1. Rutas de autorearga del navegador
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    # 2. Servir archivos multimedia (imágenes de perfil, posts, etc.) localmente
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# CONFIGURACIÓN PARA MODO PRODUCCIÓN (DEBUG = False)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]