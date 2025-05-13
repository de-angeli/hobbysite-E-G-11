from django.contrib import admin
from .models import Commission, Job, JobApplication


class JobInline(admin.TabularInline):
    model = Job

class JobApplicationInline(admin.TabularInline):
    model = JobApplication

class JobAdmin(admin.ModelAdmin):
    model = Job
    inlines = [JobApplicationInline,]
    list_display = ('commission', 'role', 'manpower_required') 
    list_filter = ('status',)

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [JobInline,]
    search_fields = ('title','description')
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ('status',)

class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = ('job', 'applicant', 'status', 'applied_on')
    list_filter = ('status',)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Job, JobAdmin)
