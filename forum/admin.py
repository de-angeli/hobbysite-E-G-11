from django.contrib import admin
from .models import PostCategory, Post


class PostInLine(admin.TabularInline):
    model = Post

class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    inlines = [PostInLine,]
    search_fields = ("name",)
    list_display = ("name",)
    list_filter = ("name",)

admin.site.register(PostCategory, PostCategoryAdmin)
