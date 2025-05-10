from django.contrib import admin
from .models import Commission, Job


class JobInline(admin.TabularInline):
    model = Job


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInline,]
    search_fields = ('title',)
    list_display = ('title', 'description',)
    list_filter = ('title', 'created_on', 'updated_on',)

admin.site.register(Commission, CommissionAdmin)
