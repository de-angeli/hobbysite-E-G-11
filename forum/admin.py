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

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title", "category", "created_on")
    list_filter = ("category", "created_on")
