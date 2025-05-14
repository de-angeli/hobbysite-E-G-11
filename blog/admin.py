from django.contrib import admin
from .models import ArticleCategory, Article, Comment

admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Comment)
