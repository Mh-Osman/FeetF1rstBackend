from django.contrib import admin
from django.urls import path, include
from .views import register_user, verify_otp,profile_view, address_list_create
from .views import login_user, logout_user, resend_otp, forgot_password, reset_password, PdfsUploadView, signupOnboardingview


urlpatterns = [

   path("register/", register_user, name="user-register"),
   path("verify-otp/", verify_otp, name="verify-otp"),
   path("login/", login_user, name="user-login"),
   path("resend-otp/", resend_otp, name="resend-otp"),
   path("forgot-password/", forgot_password, name="forgot-password"),
   path("reset-password/", reset_password, name="reset-password"),
   path("logout/", logout_user, name="user-logout"),
   path("profile/", profile_view, name="user-profile"),
   path("addresses/", address_list_create, name="address-list-create"),
   path('upload-pdf/', PdfsUploadView, name='upload-pdf'),
   path('signuponboarding/', signupOnboardingview, name='onboarding'),  # Added onboarding endpoint
  

]
  
