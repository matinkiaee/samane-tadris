from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TeacherApplication, TeachingExperience



# سفارشی‌سازی نمایش User در پنل ادمین
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'national_id', 'phone', 'role', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('national_id', 'phone', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('national_id', 'phone', 'role')}),
    )
    search_fields = ('username', 'email', 'national_id')
    ordering = ('username',)



# فرم درخواست تدریس
class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'field_of_study', 'university', 'status', 'created_at')
    list_filter = ('status', 'degree')
    search_fields = ('user__username', 'field_of_study', 'university')
    readonly_fields = ('created_at',)



# سوابق تدریس (در صورت استفاده)
class TeachingExperienceAdmin(admin.ModelAdmin):
    list_display = ('application', 'university', 'semester', 'credit_hours')
    search_fields = ('university', 'semester')

# ثبت مدل‌ها در پنل ادمین
admin.site.register(User, CustomUserAdmin)
admin.site.register(TeacherApplication, TeacherApplicationAdmin)
admin.site.register(TeachingExperience, TeachingExperienceAdmin)
