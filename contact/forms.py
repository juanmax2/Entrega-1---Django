from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
            'subject': forms.TextInput(attrs={'placeholder': '¿En qué podemos ayudarte?'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos más detalles...',
                'rows': 4, # Esto controla la altura inicial del cuadro de mensaje
            }),
        }
    