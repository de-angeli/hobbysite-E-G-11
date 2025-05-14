from django.contrib import admin
from .models import Article, ArticleCategory, Comment


class ArticleInline(admin.TabularInline):
	model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
	model = ArticleCategory
	inlines = [ArticleInline,]
	search_fields = ('name',)
	list_display = ('name',)
	list_filter = ('name',)

class ArticleAdmin(admin.ModelAdmin):
	list_display   = ('title', 'author', 'category', 'created_on', 'updated_on')
	list_filter    = ('category', 'author')
	search_fields  = ('title', 'entry')
	date_hierarchy = 'created_on'

class CommentAdmin(admin.ModelAdmin):
	list_display   = ('author', 'article', 'created_on')
	list_filter    = ('created_on',)
	search_fields  = ('entry',)
	date_hierarchy = 'created_on'

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)