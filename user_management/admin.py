from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'email')  # You can add more fields here
    search_fields = ('user__username', 'display_name', 'email')  # Allows searching by these fields

admin.site.register(Profile, ProfileAdmin)
