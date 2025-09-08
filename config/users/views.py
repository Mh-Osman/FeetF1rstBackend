from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer
from .utils import generate_otp, send_otp_email
from .models import OTP
from .models import CustomUser
from django.utils import timezone
from .utils import get_tokens_for_user # 👈 Import the function
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProfileSerializer, AddressSerializer
from .models import Profile, Address


User = get_user_model()

@api_view(['POST'])
def register_user(request):
    """
    Register a user or re-send OTP if not active.
    """
    serializer = UserRegisterSerializer(data=request.data)

    # ✅ If user already exists
    email = request.data.get("email")
    if email and User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)

        # If user already active
        if user.is_active:
            return Response({"message": "User already registered and active."}, status=400)

        # If user inactive → check OTP
        try:
            otp = OTP.objects.filter(user=user, otp_type="signup", is_used=False).latest("created_at")

            if timezone.now() < otp.expires_at:
                # OTP still valid → don't resend
                return Response({
                    "message": "Your OTP is still valid. Please verify quickly before it expires."
                }, status=200)
            else:
                # OTP expired → generate new one
                otp = generate_otp(user, otp_type="signup")
                send_otp_email(user.email, otp.code)
                return Response({
                    "message": "Previous OTP expired. A new OTP has been sent to your email."
                }, status=200)

        except OTP.DoesNotExist:
            # No OTP found → generate new
            otp = generate_otp(user, otp_type="signup")
            send_otp_email(user.email, otp.code)
            return Response({
                "message": "No valid OTP found. A new OTP has been sent to your email."
            }, status=200)

    # ✅ New user → create and send OTP
    if serializer.is_valid():
        user = serializer.save(is_active=False)

        otp = generate_otp(user, otp_type="signup")
        send_otp_email(user.email, otp.code)

        return Response({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "date_of_birth": user.date_of_birth,
            "is_partner": user.is_partner,
            "message": "OTP has been sent to your email. Please verify to activate your account."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OTP Verification
@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    code = request.data.get("code")

    if not email or not code:
        return Response({"error": "Email and OTP code are required."}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
        otp = OTP.objects.filter(user=user, code=code, otp_type="signup", is_used=False).latest("created_at")
    except (User.DoesNotExist, OTP.DoesNotExist):
        return Response({"error": "Invalid OTP or email."}, status=400)

    # Check expiry
    if timezone.now() > otp.expires_at:
        return Response({"error": "OTP expired."}, status=400)

    # Mark OTP as used + activate user
    otp.is_used = True
    otp.save()
    user.is_active = True
    user.save()

    return Response({"message": "OTP verified successfully. Account activated!"}, status=200)


@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "Login successful.",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_partner": user.is_partner,
            },
            "tokens": tokens,
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import OTP, CustomUser
from .utils import generate_otp, send_otp_email


@api_view(["POST"])
def resend_otp(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required."}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User does not exist."}, status=404)

    if user.is_active:
        return Response({"message": "User is already active."}, status=400)

    # Check last OTP
    try:
        otp = OTP.objects.filter(user=user, otp_type="signup", is_used=False).latest("created_at")
        if timezone.now() < otp.expires_at:
            return Response({"message": "Your OTP is still valid. Please check your email."}, status=200)
    except OTP.DoesNotExist:
        pass

    # Generate new OTP
    otp = generate_otp(user, otp_type="signup")
    send_otp_email(user.email, otp.code)

    return Response({"message": "A new OTP has been sent to your email."}, status=200)

@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required."}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User does not exist."}, status=404)

    # Generate password reset OTP
    otp = generate_otp(user, otp_type="reset_password")
    send_otp_email(user.email, otp.code)

    return Response({"message": "OTP for password reset sent to your email."}, status=200)


@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email")
    code = request.data.get("code")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")


    if not email or not code or not new_password:
        return Response({"error": "Email, OTP, and new password are required."}, status=400)
    if new_password and len(new_password) < 4:
        return Response({"error": "Password must be at least 4 characters long."}, status=400)
    if new_password != confirm_password:
        return Response({"error": "Password fields didn't match."}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
        otp = OTP.objects.filter(user=user, code=code, otp_type="reset_password", is_used=False).latest("created_at")
    except (CustomUser.DoesNotExist, OTP.DoesNotExist):
        return Response({"error": "Invalid email or OTP."}, status=400)

    if timezone.now() > otp.expires_at:
        return Response({"error": "OTP expired."}, status=400)

    # Use OTP once
    otp.is_used = True
    otp.save()

    # Reset password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successfully."}, status=200)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # requires SIMPLE_JWT + blacklist app
        return Response({"message": "Logged out successfully."}, status=200)
    except Exception:
        return Response({"error": "Invalid token."}, status=400)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    GET: Retrieve the logged-in user's profile.
    POST: Update the logged-in user's profile (partial updates allowed).
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return Response({"error": "Profile does not exist."}, status=404)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # elif request.method == "POST":
    #     serializer = ProfileSerializer(profile, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def address_list_create(request):
    if request.method == "GET":
        addresses = request.user.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import signupOnboardingSerializer
from .models import signupOnboarding
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signupOnboardingview(request):
    try:
        onboarding = signupOnboarding.objects.get(user=request.user)
        serializer = signupOnboardingSerializer(onboarding, data=request.data, partial=True)
    except signupOnboarding.DoesNotExist:
        serializer = signupOnboardingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            "data": serializer.data,
            "message": "Onboarding data saved successfully"
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import PdfsSerializer
from .models import Pdfs
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def PdfsUploadView(request):
    serializer = PdfsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)  # attach logged-in user
        return Response({"message": "PDF uploaded successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

