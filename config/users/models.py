from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # defaults
        extra_fields.setdefault("is_active", True)       # allow login
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

    # remove default Django fields since we use full_name
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "date_of_birth"]

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
