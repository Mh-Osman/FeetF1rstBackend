from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from .utils import generate_otp, send_otp_email

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    """
    Function-based view to register a new user.
    Creates a user, generates OTP, sends it via email.
    """
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        # 1️⃣ Create user with is_active=False
        user = serializer.save()
        user.is_active = False
        user.save()

        # 2️⃣ Generate OTP
        otp = generate_otp(user, otp_type="signup")

        # 3️⃣ Send OTP via email
        send_otp_email(user.email, otp.code)

        # 4️⃣ Return response (do NOT send OTP in production)
        return Response({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "date_of_birth": user.date_of_birth,
            "is_partner": user.is_partner,
            "message": "OTP has been sent to your email. Please verify to activate your account."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
