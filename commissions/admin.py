from django.contrib import admin
from .models import Commission, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommentInline,]
    search_fields = ('title',)
    list_display = ('title', 'description', 'people_required',)
    list_filter = ('title', 'people_required', 'created_on', 'updated_on',)

admin.site.register(Commission, CommissionAdmin)
