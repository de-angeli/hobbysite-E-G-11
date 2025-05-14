from django.contrib import admin
from .models import ThreadCategory, Thread


class PostInLine(admin.TabularInline):
    model = Thread


class PostCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    inlines = [PostInLine,]
    search_fields = ("name",)
    list_display = ("name",)
    list_filter = ("name",)

admin.site.register(ThreadCategory, PostCategoryAdmin)
