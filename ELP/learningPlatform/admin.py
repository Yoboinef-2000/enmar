# learningPlatform/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course, Lesson, Enrollment, Profile
from .forms import CourseForm, EnrollmentForm

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Status', {'fields': ('is_learner', 'is_instructor', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_learner', 'is_instructor', 'is_admin')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ('title', 'instructor', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'instructor__username', 'instructor__email')
    list_filter = ('created_at', 'updated_at')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title', 'content')
    list_filter = ('created_at', 'updated_at')

class EnrollmentAdmin(admin.ModelAdmin):
    form = EnrollmentForm
    list_display = ('learner', 'course', 'enrolled_at')
    search_fields = ('learner__username', 'learner__email', 'course__title')
    list_filter = ('enrolled_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Profile)