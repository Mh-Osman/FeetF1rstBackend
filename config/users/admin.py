from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "full_name",
        "is_active",
        "is_suspended",
        "is_partner",
        "is_staff",
    )
    list_filter = ("is_active", "is_suspended", "is_partner", "is_staff", "is_superuser")
    search_fields = ("email", "full_name")  # ✅ search by email & name
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "full_name", "date_of_birth")}),
        ("Status", {"fields": ("is_active", "is_suspended", "is_partner")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "date_of_birth", "password1", "password2", "is_active", "is_partner"),
        }),
    )


class OTPAdmin(admin.ModelAdmin):
    model = OTP
    list_display = ("user", "code", "otp_type", "created_at", "expires_at", "is_used")
    list_filter = ("otp_type", "is_used")
    search_fields = ("user__email", "code")  # ✅ search by email or OTP code
    ordering = ("-created_at",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
