from django.contrib import admin
from .models import JobVacancy, JobApplication, Contact

@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'employment_type', 'total_positions', 'filled_positions', 'available_positions', 'is_active', 'created_at']
    list_filter = ['employment_type', 'is_active', 'created_at', 'location']
    search_fields = ['title', 'location']
    list_editable = ['is_active', 'total_positions', 'filled_positions']
    readonly_fields = ['available_positions', 'is_fully_filled']
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'requirements', 'location', 'salary_range', 'employment_type')
        }),
        ('Vacancy Management', {
            'fields': ('total_positions', 'filled_positions', 'available_positions', 'is_fully_filled', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def available_positions(self, obj):
        return obj.available_positions
    available_positions.short_description = 'Available Positions'
    
    actions = ['mark_as_active', 'mark_as_inactive', 'reset_filled_positions']
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} job(s) marked as active.")
    mark_as_active.short_description = "Mark selected jobs as active"
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} job(s) marked as inactive.")
    mark_as_inactive.short_description = "Mark selected jobs as inactive"
    
    def reset_filled_positions(self, request, queryset):
        queryset.update(filled_positions=0)
        self.message_user(request, f"Reset filled positions for {queryset.count()} job(s).")
    reset_filled_positions.short_description = "Reset filled positions to 0"

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job_vacancy', 'email', 'phone', 'applied_at']
    list_filter = ['job_vacancy', 'applied_at']
    search_fields = ['full_name', 'email', 'job_vacancy__title']
    readonly_fields = ['applied_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )
