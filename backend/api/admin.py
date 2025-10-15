from django.contrib import admin
from django.utils import timezone
from .models import (
    Program, Gallery, Testimonial, Event, Branch, 
    Inquiry, Blog, TeamMember, FAQ, Setting,
    AboutPage, AboutFeature, HomeSlider, HomeStats, Admission
)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'age_group', 'created_at']
    list_filter = ['age_group', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'category', 'created_at']
    list_filter = ['type', 'category', 'created_at']
    search_fields = ['title', 'category']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'relation', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['parent_name', 'relation', 'message']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['title', 'description']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'address']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'phone', 'child_age', 'branch', 'created_at']
    list_filter = ['branch', 'created_at']
    search_fields = ['parent_name', 'phone', 'message']
    readonly_fields = ['created_at']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'created_at']
    search_fields = ['name', 'role']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['question', 'answer']
    ordering = ['order', 'question']


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['key', 'value', 'description']


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    search_fields = ['title', 'subtitle', 'mission_content', 'vision_content']
    
    def has_add_permission(self, request):
        # Only allow one AboutPage instance
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False


@admin.register(AboutFeature)
class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['category', 'order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Organization', {
            'fields': ('category', 'order', 'is_active')
        }),
    )


@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'order', 'is_active', 'created_at']
    list_filter = ['media_type', 'is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'media_type')
        }),
        ('Media', {
            'fields': ('image', 'video', 'video_poster'),
            'description': 'Upload either an image or video. For videos: max 15 seconds duration, MP4/MOV/AVI format, max 50MB file size. You can also upload a poster image that will be shown before the video loads.'
        }),
        ('Button Settings', {
            'fields': ('button_text', 'button_url')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(HomeStats)
class HomeStatsAdmin(admin.ModelAdmin):
    list_display = ['stat_type', 'value', 'suffix', 'label', 'order', 'is_active', 'updated_at']
    list_filter = ['stat_type', 'is_active', 'created_at']
    search_fields = ['label', 'stat_type']
    list_editable = ['value', 'suffix', 'order', 'is_active']
    ordering = ['order', 'stat_type']
    
    fieldsets = (
        ('Stat Information', {
            'fields': ('stat_type', 'value', 'suffix', 'label')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color', 'order', 'is_active')
        }),
    )


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['student_full_name', 'parent_full_name', 'preferred_program', 'status', 'submitted_at']
    list_filter = ['status', 'preferred_program', 'submitted_at', 'student_gender']
    search_fields = ['student_first_name', 'student_last_name', 'parent_first_name', 'parent_last_name', 'parent_email']
    list_editable = ['status']
    readonly_fields = ['submitted_at', 'updated_at']
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_first_name', 'student_last_name', 'student_date_of_birth', 'student_gender')
        }),
        ('Parent/Guardian Information', {
            'fields': ('parent_first_name', 'parent_last_name', 'parent_email', 'parent_phone', 'parent_relationship')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Program Information', {
            'fields': ('preferred_program', 'preferred_start_date', 'current_school')
        }),
        ('Medical Information', {
            'fields': ('medical_conditions', 'medications', 'emergency_medical_consent')
        }),
        ('Additional Information', {
            'fields': ('special_needs', 'previous_preschool_experience', 'why_choose_us')
        }),
        ('Application Status', {
            'fields': ('status', 'notes', 'reviewed_at', 'reviewed_by')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            obj.reviewed_at = timezone.now()
            obj.reviewed_by = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)
