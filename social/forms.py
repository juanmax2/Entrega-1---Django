from django import forms
from django.contrib.auth.models import User
from crispy_forms.layout import Layout, Div, Field, Submit
from crispy_forms.helper import FormHelper
from profiles.models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta: 
        model = User
        fields = [
            'first_name',
            'username',
            'email',
            'password'
        ]
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estilo_input = "mb-3 appearance-none border-t-0 border-l-0 border-r-0 border-b border-pink-500 focus:ring-0 focus:border-pink-700"
    
   
        for field in self.fields.values():
            field.widget.attrs.update({'class': estilo_input})
            field.help_text = "" 

        self.helper = FormHelper()
        self.helper.form_class = 'border p-8'
        self.helper.layout = Layout(
            'username',
            'first_name',
            'email',
            'password',
            Submit('submit', 'Registrarse', css_class="bg-pink-200 text-black rounded-2xl mt-3")
        )
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
            
        if commit:
            user.save()
            from profiles.models import UserProfile
            UserProfile.objects.create(user=user)
                
        return user
        

class LoginForm(forms.Form):
    
    username = forms.CharField(label = 'Nombre de usuario')
    password = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estilo_input = "mb-3 px-2 appearance-none border-t-0 border-l-0 border-r-0 border-b border-pink-500 focus:ring-0 focus:border-pink-700"
        
    
        for field in self.fields.values():
            field.widget.attrs.update({'class': estilo_input})
            field.help_text = "" 

        self.helper = FormHelper()
        self.helper.form_class = 'border p-8'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Registrarse', css_class="bg-pink-200 text-black rounded-2xl mt-3")
        )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'birth_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({
            'class': (
                "border rounded-2xl p-1 border-pink-300 text-pink-300" 
            )
        })
        
class ProfileFollow(forms.Form):
    profile_pk = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.CharField(widget=forms.HiddenInput())