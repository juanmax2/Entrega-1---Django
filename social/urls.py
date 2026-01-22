
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
# if not settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
# else:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     # Include django_browser_reload URLs only in DEBUG mode
#     urlpatterns += [
#         path("__reload__/", include("django_browser_reload.urls")),
#     ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if not settings.DEBUG:
    urlpatterns += [
        # Nota que hemos quitado el / inicial del r'^media...
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        # También para estáticos por si WhiteNoise falla en local
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

# if settings.DEBUG:
#     # En desarrollo, Django sirve media automáticamente
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     # URLs de autoreload
#     urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
# else:
#     # En producción/build (DEBUG=False), forzamos el servido de media
#     urlpatterns += [
#         re_path(r'^/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
#     ]