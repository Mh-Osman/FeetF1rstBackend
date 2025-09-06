from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # defaults
        extra_fields.setdefault("is_active", False)       # allow login
        extra_fields.setdefault("is_suspended", False)   # not suspended
        extra_fields.setdefault("is_partner", False)     # normal user by default

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_suspended", False)
        extra_fields.setdefault("is_partner", False)  # superuser usually not partner

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    # status flags
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    # timestamps
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "date_of_birth"]
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    otp_type = models.CharField(
        max_length=20,
        choices=[
            ("login", "Login"),
            ("signup", "Signup"),
            ("reset_password", "Reset Password"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code} ({self.otp_type})"

def profile_image_upload_path(instance, filename):
    # Example: profile_images/user_1/default.png
    return f"profile_images/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        default='default_profile.png'
    )
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} Profile"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    first_name = models.CharField(max_length=100 , default="")  # default added to avoid issues with existing records
    last_name = models.CharField(max_length=100 , default="")   # default added to avoid issues with existing records
    street_address = models.CharField(max_length=255)
    additional_address = models.CharField(max_length=255, blank=True, null=True)  # optional
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.street_address}, {self.city}, {self.country}"
class signupOnboarding(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='onboarding')
    
    how_did_you_hear = models.JSONField(blank=True, null=True )  # "Come ha scoperto FeetF1rst?" - can be multiple selections
    favorite_products = models.CharField(max_length=255, blank=True, null=True)  # "Quali sono i prodotti che utilizzi di più?"
    foot_or_shoe_issues = models.CharField(max_length=255, blank=True, null=True)  # "C'è qualcosa riguardo a problemi ai piedi o scarpe non adatte?"
   
    
    def __str__(self):
        return f"{self.user.full_name}'s Onboarding Responses"
    
class Pdfs(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pdfs')
    file = models.FileField(upload_to='user_pdfs/')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PDF for {self.user.full_name} uploaded at {self.uploaded_at}"
    