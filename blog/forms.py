from django import forms
from .models import Article, Comment, ArticleImage


class ArticleForm(forms.ModelForm):
    new_gallery_image = forms.ImageField(required=False, label="Add Image to Gallery")

    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
