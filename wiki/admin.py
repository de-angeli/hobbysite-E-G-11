from django.contrib import admin
from .models import Article, ArticleCategory

class ArticleInline(admin.TabularInline):
  model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
  model = ArticleCategory
  inlines = [ArticleInline,]
  search_fields = ('name',)
  list_display = ('name',)
  list_filter = ('name',)


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
