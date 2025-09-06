import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import OTP
from rest_framework_simplejwt.tokens import RefreshToken

def generate_otp(user, otp_type="signup"):
    code = f"{random.randint(1000, 9999)}"
    expires_at = timezone.now() + timedelta(minutes=5)
    otp = OTP.objects.create(
        user=user,
        code=code,
        otp_type=otp_type,
        expires_at=expires_at
    )
    return otp

def send_otp_email(email, code):
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {code}. It expires in 5 minutes.",
        from_email="no-reply@example.com",
        recipient_list=[email],
    )




def get_tokens_for_user(user):
    """
    Generates JWT refresh and access tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }