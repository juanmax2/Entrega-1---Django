from .models import Post, Comment
from django import forms

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'image',
            'caption',
        ]
        widgets = {
            
            'image': forms.FileInput(attrs={
                'class':  "border rounded-2xl p-1 border-pink-600 text-pink-600 hover:border-white hover:text-white hover:bg-pink-600"
                
        }),
            'caption': forms.Textarea(attrs={
                'class': " p-3"
            })
        }
    
   
   
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        
        widgets = {
            'text': forms.Textarea(attrs={
                'class': " p-3"
            })
        }