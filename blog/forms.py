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
            "title": forms.TextInput(attrs={'class': 'form-control rounded-3 py-2'}),
            "text": CKEditor5Widget(config_name="post"),
        }
        labels = {
            'title': 'Título',
            'text': 'Contenido',
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control w-100 rounded-3 py-2', 
            'placeholder': 'Tu nombre de usuario'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control w-100 rounded-3 py-2', 
            'placeholder': '••••••••'
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control rounded-3 py-2', 
				'placeholder': 'Tu nombre o apodo...'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control rounded-3', 
                'rows': 4, 'placeholder': 'Escribe tu comentario aquí...'
			}),
        }
        labels = {
            'author': 'Autor',
            'text': 'Contenido',
        }
