"""
URL configuration for Poh_pih_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static
from Pih_poh_app.views import HomeView,SignupListView,SignupCreateView,LoginAPIView,DanceLevelListView, DanceLevelCreateView, DanceLevelUpdateView, DanceLevelDeleteView,InterestLevelListView, InterestLevelCreateView, InterestLevelUpdateView,InterestLevelDeleteView,StyleLevelListView, StyleLevelCreateView, StyleLevelUpdateView, StyleLevelDeleteView,GetUserInterest, PostUserInterest, PutUserInterest, DeleteUserInterest , UserProfileView,CreateProfilePictureView, UpdateUserProfileView,UpdateProfilePictureView, ChangePasswordView,DeleteAccountView,facebook_login,SubscriptionPlanListView, MySubscriptionView, UpdateUserSubscriptionView,CreateSubscription,CreatePaymentIntent, PaymentStatusView, RefundPaymentView,CancelSubscriptionView,MyPaymentsView, UsageTrackingView,CheckVideoLimitView,GoogleLoginView,ForgotPasswordView,ResetPasswordView,LogoutAPIView,GetJWTTokenAPIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",HomeView.as_view(),name="home"),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    path('delete-my-data/', TemplateView.as_view(template_name='delete_my_data.html')),

    # Signup & Login APIs

    path('get/signup/', SignupListView.as_view(), name='signup-list'),

    path('post/signup/', SignupCreateView.as_view(), name='signup-create'),

    path('post/login/', LoginAPIView.as_view(), name='login'),

    #Dancelevel 

    path('GetDancelevel/', DanceLevelListView.as_view(), name='DanceLevel-list'),
    
    path('PostDancelevel/', DanceLevelCreateView.as_view(), name='DanceLevel-create'),

    path('PutDancelevel/<int:id>/', DanceLevelUpdateView.as_view(), name='DanceLevel-update'),  # PUT for update

    path('DeleteDancelevel/<int:id>/', DanceLevelDeleteView.as_view(), name='DanceLevel-delete'),  # DELETE for delete

    # Interest Level URLs
    path('GetInterest/', InterestLevelListView.as_view(), name='InterestLevel-list'),

    path('PostInterest/', InterestLevelCreateView.as_view(), name='InterestLevel-create'),

    path('PutInterest/<int:id>/', InterestLevelUpdateView.as_view(), name='InterestLevel-update'),  # PUT for update

    path('DeleteInterest/<int:id>/', InterestLevelDeleteView.as_view(), name='InterestLevel-delete'),  # DELETE for delete

    # Style Level URLs
    path('GetStyle/', StyleLevelListView.as_view(), name='StyleLevel-list'),

    path('PostStyle/', StyleLevelCreateView.as_view(), name='StyleLevel-create'),

    path('PutStyle/<int:id>/', StyleLevelUpdateView.as_view(), name='StyleLevel-update'),  # PUT for update

    path('DeleteStyle/<int:id>/', StyleLevelDeleteView.as_view(), name='StyleLevel-delete'),  # DELETE for delete

    # User Interest
    path('GetUserInterest/', GetUserInterest.as_view(), name='get_user_interest'),
     
    path('PostUserInterest/', PostUserInterest.as_view(), name='post_user_interest'), 

    path('PutUserInterest/<int:id>/', PutUserInterest.as_view(), name='put_user_interest'), 

    path('DeleteUserInterest/<int:id>/', DeleteUserInterest.as_view(), name='delete_user_interest'),

    #profile management

    path('profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),

    path('profile/update/<int:id>/', UpdateUserProfileView.as_view(), name='update-profile'),

    # path('profile/upload-picture/<int:id>/', UploadProfilePictureView.as_view(), name='upload-profile-picture'),

    # Create profile picture (for first-time uploads)
    path('profile/upload-picture/<int:id>/', CreateProfilePictureView.as_view(), name='create-profile-picture'),
    
    # Update profile picture (for existing users)
    path('profile/update-picture/<int:id>/', UpdateProfilePictureView.as_view(), name='upload-profile-picture'),

    path('profile/change-password/<int:id>/', ChangePasswordView.as_view(), name='change-password'),

    path('profile/delete-account/<int:id>/', DeleteAccountView.as_view(), name='delete-account'),

    # Auth URLs

    path('auth/', include('dj_rest_auth.urls')),  # REST auth endpoints
    path('auth/social/', include('allauth.socialaccount.urls')),  # Social auth endpoints
    # Add Django allauth authentication URLs
    path('accounts/', include('allauth.urls')),  # This adds the missing `/accounts/login/`
    path('auth/', include('social_django.urls', namespace='social')),

    path('facebook-login/', facebook_login, name='facebook_login'),
# new login google endpoint
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/', include('dj_rest_auth.urls')),  # Includes login/logout endpoints
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Includes signup
    path('auth/google/token/', GoogleLoginView.as_view(), name='google_login_token'),
    # path('accounts/google/login/callback/', include('allauth.urls')),

# https://accounts.google.com/o/oauth2/auth?client_id=962172872566-bqqcrj3krd12dp29loutui7gm0pn8855.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback&response_type=token&scope=email profile&access_type=offline
# i need to create api in django so user can click on login button then they will redirect the googel page , then they can login with google and they can access website and after login one jwt token should be generated so using this token they can access profile 
# https://accounts.google.com/o/oauth2/v2/auth?
# client_id=962172872566-bqqcrj3krd12dp29loutui7gm0pn8855.apps.googleusercontent.com
# &redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback
# &response_type=token
# &scope=email profile openid
# https://accounts.google.com/o/oauth2/v2/auth?client_id=962172872566-bqqcrj3krd12dp29loutui7gm0pn8855.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback&response_type=token&scope=email profile openid



    # http://127.0.0.1:8000/accounts/google/login/
    # http://127.0.0.1:8000/accounts/facebook/login/
    #https://poh-pih.onrender.com/accounts/facebook/login/
    # https://dashboard.render.com/web/srv-cv8oegin91rc738llg00/deploys/dep-cv8sae1c1ekc7382murg
    

    # payment and subscription related urls 

    path('plans/', SubscriptionPlanListView.as_view()),

    path('my-subscription/', MySubscriptionView.as_view()),

    path('update-subscription/', UpdateUserSubscriptionView.as_view()),

    path('create-subscription/', CreateSubscription.as_view()),

    path('create-payment-intent/', CreatePaymentIntent.as_view()),

    path('payment-status/<str:payment_intent_id>/', PaymentStatusView.as_view()),

    path('refund-payment/<str:payment_intent_id>/', RefundPaymentView.as_view()),

    path('cancel-subscription/', CancelSubscriptionView.as_view()),

    path('list-my-payments/', MyPaymentsView.as_view()),
    
    path('usage-tracking/', UsageTrackingView.as_view()),

    path('check-video-limit/', CheckVideoLimitView.as_view()),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),

    # path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/get-token/', GetJWTTokenAPIView.as_view(), name='get-token'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

