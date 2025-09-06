from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import Profile, Address, signupOnboarding
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=4)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=4)

    class Meta:
        model = User
        fields = ["email", "full_name", "date_of_birth", "password", "confirm_password", "is_partner"]
        extra_kwargs = {"is_partner": {"default": False}}
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(_("Invalid email or password."))
            if not user.is_active:
                raise serializers.ValidationError(_("Account is not active. Please verify OTP."))
            if user.is_suspended:
                raise serializers.ValidationError(_("Account is suspended. Contact support."))
        else:
            raise serializers.ValidationError(_("Must include 'email' and 'password'."))

        data["user"] = user
        return data




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","profile_image", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "user", "first_name", "last_name", "street_address",
                  "additional_address", "postal_code", "city", "phone_number", "country"]
        read_only_fields = ["id", "user"]

class signupOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = signupOnboarding
        fields = ["id", "user", "how_did_you_hear", "favorite_products", "foot_or_shoe_issues"]
        read_only_fields = ["id", "user"]
from .models import Pdfs
class PdfsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdfs
        fields = ['id', 'user', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'user',]