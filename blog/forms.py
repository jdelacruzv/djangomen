from django import forms
from .models import Post

class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ('title', 'text')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
