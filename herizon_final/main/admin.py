from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Post, Comment, Job, Material, Badge

# ---------------------------
# Badge Inline for UserProfile
# ---------------------------
class BadgeInline(admin.TabularInline):
    model = Badge
    extra = 1  # allows adding one badge inline by default
    readonly_fields = ()

# ---------------------------
# UserProfile Admin
# ---------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified', 'batch', 'saved_jobs_count', 'saved_materials_count')
    list_editable = ('verified', 'batch')
    search_fields = ('user__username', 'skills', 'batch')
    list_filter = ('verified', 'batch', 'gender')
    inlines = [BadgeInline]  # show badges inline

    # Fields to show in the edit page
    fields = ('user', 'gender', 'bio', 'skills', 'linkedin', 'verified', 'batch', 'saved_jobs', 'saved_materials')

    filter_horizontal = ('saved_jobs', 'saved_materials')  # better UI for M2M fields

    def saved_jobs_count(self, obj):
        return obj.saved_jobs.count()
    saved_jobs_count.short_description = 'Saved Jobs'

    def saved_materials_count(self, obj):
        return obj.saved_materials.count()
    saved_materials_count.short_description = 'Saved Materials'

# ---------------------------
# Post, Comment, Job Admin
# ---------------------------
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Job)

# ---------------------------
# Material Admin with file preview
# ---------------------------
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'created_at', 'file_preview')
    search_fields = ('title', 'category', 'uploaded_by__username')
    list_filter = ('category', 'uploaded_by', 'created_at')
    readonly_fields = ('file_preview',)

    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'link', 'file', 'uploaded_by', 'file_preview')
        }),
    )

    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📂 View File</a>', obj.file.url)
        elif obj.link:
            return format_html('<a href="{}" target="_blank">🔗 Open Link</a>', obj.link)
        return "-"
    file_preview.short_description = 'Preview'

# ---------------------------
# Badge Admin (optional separate view)
# ---------------------------
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__user__username')
