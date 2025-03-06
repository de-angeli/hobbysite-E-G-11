from django.contrib import admin
from .models import ArticleCategory, Article

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') 

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'updated_on')  
    list_filter = ('category',)  
    search_fields = ('title', 'entry') 
