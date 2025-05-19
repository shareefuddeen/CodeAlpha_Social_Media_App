from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Comment,Profile

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreatePostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields= ["title","content"]

class commentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]
        
class update_profile_form(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ["bio","avatar"]