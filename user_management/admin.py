from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'email')
    search_fields = ('user__username', 'display_name', 'email')

admin.site.register(Profile, ProfileAdmin)
