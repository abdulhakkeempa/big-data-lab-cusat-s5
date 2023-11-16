from django.contrib import admin
from accounts.models import User
# Register your models here.
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "date_of_birth", "is_active", "is_staff")
    readonly_fields = ["date_joined"]

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "date_of_birth", "password1", "password2", "is_active", "is_staff")}
        ),
    )

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')})  # Include 'groups' and 'user_permissions' fields
    )

    exclude = ('password',)

admin.site.register(User, CustomUserAdmin)
