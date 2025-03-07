from django.contrib import admin
from .models import ArticleCategory, Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ('name', 'description')


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category',)
    search_fields = ('title', 'entry')

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
