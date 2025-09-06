from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP, Profile, Address, Pdfs

@admin.register(CustomUser)
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

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    model = OTP
    list_display = ("user", "code", "otp_type", "created_at", "expires_at", "is_used")
    list_filter = ("otp_type", "is_used")
    search_fields = ("user__email", "code")  # ✅ search by email or OTP code
    ordering = ("-created_at",)


# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(OTP, OTPAdmin)

from django.utils.html import format_html
from django.contrib.admin import ModelAdmin
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    model = Profile

    list_display = ['user', 'profile_picture_tag', ]  # list view

    # readonly_fields = ['profile_picture_tag']  # show image in detail view

    # Method to display image
    def profile_picture_tag(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width:100px; height:100px; object-fit:cover; border-radius:50%"/>',
                obj.profile_image.url
            )
        return "-"
    profile_picture_tag.short_description = 'profile_image'





@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "street_address", "city", "country", "phone_number")
    search_fields = ("user__email", "first_name", "last_name", "street_address", "city", "country")
    list_filter = ("city", "country")

@admin.register(Pdfs)
class PdfsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_link', 'uploaded_at')
    readonly_fields = ('id', 'uploaded_at', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download PDF</a>', obj.file.url)
        return "No File"
    file_link.short_description = "PDF File"


from .models import signupOnboarding
@admin.register(signupOnboarding)
class signupOnboardingAdmin(admin.ModelAdmin):
    # Columns in the list view
    list_display = ('user', 'how_did_you_hear_clickable', 'favorite_products', 'foot_or_shoe_issues')
    
    # Make the clickable field read-only
    readonly_fields = ('id','how_did_you_hear_clickable', 'favorite_products', 'foot_or_shoe_issues')
    
    # Hide raw JSON field from admin form
    exclude = ('how_did_you_hear',)

    # Specify order of fields in detail/edit form
    #fields = ('how_did_you_hear_clickable', 'favorite_products', 'foot_or_shoe_issues')

    # Display how_did_you_hear as clickable items
    def how_did_you_hear_clickable(self, obj):
        if obj.how_did_you_hear:
            items = [f'<a href="#">{item}</a>' for item in obj.how_did_you_hear]
            return format_html(", ".join(items))
        return "No Response"
    
    how_did_you_hear_clickable.short_description = "How did you hear about FeetF1rst?"