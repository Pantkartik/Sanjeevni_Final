"""
Admin interface for users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for UserProfile model.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    """
    Custom User admin that includes UserProfile.
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active')
    list_filter = ('profile__role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_role(self, obj):
        return getattr(obj.profile, 'role', 'N/A')
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ('user', 'role', 'full_name', 'phone_number', 'date_of_birth', 'created_at')
    list_filter = ('role', 'gender', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'phone_number', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_contact_name')
        }),
        ('Health Information', {
            'fields': ('blood_type', 'allergies', 'medical_conditions', 'current_medications')
        }),
        ('Technical', {
            'fields': ('profile_picture', 'firebase_token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
