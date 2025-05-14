from django.contrib import admin
from .models import ArticleCategory, Article, Comment


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ('name', 'description')


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category',)
    search_fields = ('title', 'entry')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_on')
    list_filter = ('created_on', 'article')
    search_fields = ('entry', 'author__user__username')

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
