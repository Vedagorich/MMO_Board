from django import forms
from django.forms import ModelForm, CharField, HiddenInput
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'categories', 'user']
        widgets = {
            'user': forms.HiddenInput(),
        }
        labels = {
            'title': _('Заголовок'),
            'categories': _('Категория'),
            'content': _('Объявление'),
            'image': _('Изображение')
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }



