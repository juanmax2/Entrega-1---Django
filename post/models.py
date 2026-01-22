from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User,verbose_name='Usuario', on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(verbose_name='Imagen', upload_to='post_images/')
    caption = models.TextField(verbose_name='Descripción', max_length=500, blank=True)
    created_at = models.DateTimeField(verbose_name='Fecha de creación',auto_now_add=True)
    likes = models.ManyToManyField(User, verbose_name='Número de likes', blank=True, related_name='liked_posts')
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500, verbose_name='Escribe tu comentario')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        
    def __str__(self):
        return f"Comentado por {self.user.username} - {self.post}"