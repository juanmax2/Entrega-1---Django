from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil',upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField('Biografía', max_length=500, blank=True)
    birth_date = models.DateField('Fecha nacimiento',null=True, blank=True)
    follows = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers',
        through='Follow'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        
    def __str__(self):
        return self.user.username
    
    @property
    def get_avatar_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return "/theme/img/no_picture.png"
    
    def follow(self, profile):
        Follow.objects.get_or_create(follower=self, following=profile)
        
    def unfollow(self, profile):
        return Follow.objects.filter(follower=self, following=profile).delete()
    
    

class Follow(models.Model):
    follower =  models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower','following')
        
    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'