from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Post, Comment
from .richtext import sanitize_rich_text


class PostForm(forms.ModelForm):
    def clean_text(self):
        return sanitize_rich_text(self.cleaned_data["text"])

    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            "text": CKEditor5Widget(config_name="post"),
        }
        labels = {
            'title': 'Título',
            'text': 'Contenido',
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        labels = {
            'author': 'Autor',
            'text': 'Contenido',
        }
