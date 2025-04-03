import stripe
import requests
from django.shortcuts import render
from django.views import View 
from rest_framework import generics
from datetime import datetime
from django.http import JsonResponse
from django.db import transaction
from .serializers import SignupSerializer,LoginSerializer,DanceLevelSerializer,IntersetSerializer,StyleSerializer,UserInterestSerializer,UserProfileSerializer, UpdateUserProfileSerializer,UploadProfilePictureSerializer, ChangePasswordSerializer,SubscriptionPlanSerializer, UserSubscriptionSerializer, PaymentSerializer, UsageTrackingSerializer
from .models import DanceLevel, Interest, Style,UserInterest,Payment,SubscriptionPlan, UserSubscription,CustomUser,UsageTracking
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrAdmin
from django.contrib.auth import get_user_model
User = get_user_model()  # Get the custom user model
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY  # Ensure Stripe is configured



class HomeView(View):
    def get(self,request):
        return render(request,'home.html')

class SignupListView(generics.ListAPIView):
    queryset = User.objects.all()  # Now it correctly references CustomUser
    serializer_class = SignupSerializer

class SignupCreateView(generics.CreateAPIView):  
    queryset = User.objects.all()  
    serializer_class = SignupSerializer

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    authentication_classes = []  # Disable authentication for login
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                "message": "Login successful",
                "token": access_token,
                "user_id": user.id,  # Add the user id to the response
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DanceLevel Views
class DanceLevelListView(generics.ListAPIView):
    queryset = DanceLevel.objects.all()
    serializer_class = DanceLevelSerializer

class DanceLevelCreateView(generics.CreateAPIView):
    queryset = DanceLevel.objects.all()
    serializer_class = DanceLevelSerializer

class DanceLevelUpdateView(generics.UpdateAPIView):
    queryset = DanceLevel.objects.all()
    serializer_class = DanceLevelSerializer
    lookup_field = 'id'  # You can update using the 'id' field

class DanceLevelDeleteView(generics.DestroyAPIView):
    queryset = DanceLevel.objects.all()
    serializer_class = DanceLevelSerializer
    lookup_field = 'id'  # Delete using 'id'

# Interest Views
class InterestLevelListView(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = IntersetSerializer

class InterestLevelCreateView(generics.CreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = IntersetSerializer

class InterestLevelUpdateView(generics.UpdateAPIView):
    queryset = Interest.objects.all()
    serializer_class = IntersetSerializer
    lookup_field = 'id'

class InterestLevelDeleteView(generics.DestroyAPIView):
    queryset = Interest.objects.all()
    serializer_class = IntersetSerializer
    lookup_field = 'id'

# Style Views
class StyleLevelListView(generics.ListAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer

class StyleLevelCreateView(generics.CreateAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer

class StyleLevelUpdateView(generics.UpdateAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    lookup_field = 'id'

class StyleLevelDeleteView(generics.DestroyAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    lookup_field = 'id'

class GetUserInterest(generics.ListAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer

class PostUserInterest(generics.CreateAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer

class PutUserInterest(generics.UpdateAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    lookup_field = 'id' 

class DeleteUserInterest(generics.DestroyAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    lookup_field = 'id'  

#Profile management related views

class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = "id"

class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = "id"


# class UploadProfilePictureView(generics.UpdateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UploadProfilePictureSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
#     lookup_field = "id"
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UploadProfilePictureSerializer
from .permissions import IsOwnerOrAdmin

class CreateProfilePictureView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UploadProfilePictureSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Ensure the user is authenticated and authorized
    lookup_field = 'id'

    # def perform_create(self, serializer):
    #     user = self.request.user  # Get the currently logged-in user
    #     # Save the profile picture for the logged-in user
    #     serializer.save(user=user)  # Save the profile picture and associate with the logged-in user

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UploadProfilePictureSerializer
from .permissions import IsOwnerOrAdmin  # Ensure this is defined in your project

class UpdateProfilePictureView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UploadProfilePictureSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Allow only authenticated and authorized users
    lookup_field = "id"

    # def perform_update(self, serializer):
    #     user = self.request.user
    #     serializer.save(user=user)  # Associate the profile picture with the logged-in user


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = "id"
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Ensure only logged-in users can delete
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "Your account has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class GetJWTTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.first_name
            }
        })

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Perform logout by invalidating the token
            request.auth.delete()  # Delete the token to log out
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({"message": "Already logged out"}, status=status.HTTP_400_BAD_REQUEST)
# from dj_rest_auth.views import LoginView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from allauth.socialaccount.models import SocialAccount

# class GoogleLoginView(LoginView):
#     def post(self, request, *args, **kwargs):
#         # Call default login view logic
#         response = super().post(request, *args, **kwargs)

#         # Get the logged-in user
#         user = self.request.user

#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         # Return JWT token along with default response
#         return Response({
#             "user": {
#                 "id": user.id,
#                 "email": user.email,
#                 "username": user.username
#             },
#             "access_token": access_token,
#             "refresh_token": str(refresh)
#         })

import google.auth.transport.requests
import google.oauth2.id_token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginView(APIView):
    def post(self, request):
        try:
            # Get the access token from request
            access_token = request.data.get("access_token")
            if not access_token:
                return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify Google ID Token
            google_request = google.auth.transport.requests.Request()
            decoded_token = google.oauth2.id_token.verify_oauth2_token(access_token, google_request)

            if not decoded_token:
                return Response({"error": "Invalid Google access token"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract user information from Google token
            email = decoded_token.get("email")
            first_name = decoded_token.get("given_name", "")
            last_name = decoded_token.get("family_name", "")

            if not email:
                return Response({"error": "Google token missing email"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already exists, else create one
            user, created = User.objects.get_or_create(email=email, defaults={"username": email, "first_name": first_name, "last_name": last_name})

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# login with facebook api view 

@api_view(['POST'])
def facebook_login(request):
    access_token = request.data.get('access_token')
    fb_url = f'https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}'
    fb_response = requests.get(fb_url)
    data = fb_response.json()
    if 'error' in data:
        return Response({'error': 'Invalid Facebook token'}, status=400)
    email = data.get('email')
    name = data.get('name')
    user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name})
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': user.username})

# payment and subscription related apis view 

class CreateSubscription(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user  # Ensure user is authenticated
            plan_type = request.data.get('plan_type')  # 'free', 'standard', 'premium'

            if plan_type not in ['free', 'standard', 'premium']:
                return Response({"error": "Invalid plan type"}, status=status.HTTP_400_BAD_REQUEST)

            # Map your actual Stripe Price IDs to plan types
            price_id_map = {
                'free': 'price_1FreePlanXYZ123',  # Replace with your actual Stripe Price IDs
                'standard': 'price_1StandardPlanXYZ456',
                'premium': 'price_1PremiumPlanXYZ789'
            }
            video_limit_map = {
                'free': 1,
                'standard': 3,
                'premium': None  # Use None for unlimited videos instead of float('inf')
            }
            # Check if user already has an active subscription
            existing_subscription = Payment.objects.filter(user=user, status="active").first()
            if existing_subscription:
                return Response({"error": "You already have an active subscription"}, status=status.HTTP_400_BAD_REQUEST)
            # Ensure the user has a Stripe customer ID
            if not getattr(user, 'stripe_customer_id', None):  # More reliable check
                stripe_customer = stripe.Customer.create(
                    email=user.email,
                    name=user.get_full_name()
                )
                user.stripe_customer_id = stripe_customer.id
                user.save()

            # Create the Stripe subscription
            subscription = stripe.Subscription.create(
                customer=user.stripe_customer_id,
                items=[{"price": price_id_map[plan_type]}],
                expand=["latest_invoice.payment_intent"]
            )

            # Save subscription to the database
            Payment.objects.create(
                user=user,
                subscription_id=subscription["id"],
                product_id=subscription["items"]["data"][0]["price"]["product"],
                plan_type=plan_type,
                video_limit=video_limit_map[plan_type],
                amount=subscription["items"]["data"][0]["price"]["unit_amount"] / 100,
                currency=subscription["items"]["data"][0]["price"]["currency"],
                status=subscription["status"],
                subscription_start_date=timezone.now(),
                subscription_end_date=timezone.now() + timedelta(days=30)
            )

            #  Create UserSubscription entry
            UserSubscription.objects.create(
                user=user,
                plan=SubscriptionPlan.objects.get(plan_name=plan_type),
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=30)
            )

            return Response({
                "subscription_id": subscription["id"],
                "status": subscription["status"],
                "plan_type": plan_type
            }, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            return Response({"error": str(e.user_message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            payment = Payment.objects.filter(user=request.user, is_active=True).last()
            if not payment or not payment.subscription_id:
                return Response({"error": "No active subscription found"}, status=404)
            stripe.Subscription.delete(payment.subscription_id)
            payment.is_active = False
            payment.save()
            UserSubscription.objects.filter(user=request.user, is_active=True).update(is_active=False)
            return Response({"message": "Subscription cancelled successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated]

class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sub = UserSubscription.objects.filter(user=request.user, is_active=True).last()
        if not sub:
            return Response({"error": "No active subscription"}, status=404)
        return Response(UserSubscriptionSerializer(sub).data)

class UpdateUserSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        plan_id = request.data.get('plan_id')
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
            with transaction.atomic():  # Ensuring atomicity
                UserSubscription.objects.create(
                    user=request.user,
                    plan=plan,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=30)
                )
            return Response({"message": "Subscription updated successfully"})
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Invalid Plan ID"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)



class CreatePaymentIntent(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    def post(self, request):
        try:
            user = request.user              
            # Ensure user is authenticated
            if not user.is_authenticated:
                return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            amount = int(request.data.get('amount', 0))
            currency = request.data.get('currency', 'usd')
            subscription_id = request.data.get('subscription_id', None)
            product_id = request.data.get('product_id', None)
            # Create a PaymentIntent in Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=["card"],
            )
            # Save payment details in the database
            Payment.objects.create(
                user=user,
                payment_intent_id=intent["id"],
                client_secret=intent["client_secret"],
                subscription_id=subscription_id,
                product_id=product_id,
                amount=amount,
                currency=currency,
                status=intent["status"],
                payment_method=None,
                refund_status='not_refunded'
            )
            return Response({
                "payment_intent_id": intent["id"],
                "clientSecret": intent["client_secret"]
            }, status=status.HTTP_200_OK)        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        if event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            payment = Payment.objects.get(payment_intent_id=payment_intent["id"])
            payment.status = "succeeded"
            payment.save()
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Webhook signature verification failed"}, status=400)
    return JsonResponse({"status": "success"})

class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, payment_intent_id):
        try:
            # Retrieve the PaymentIntent from Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Update status and payment method in the database
            payment = Payment.objects.get(payment_intent_id=payment_intent_id)
            payment.status = intent["status"]
            payment.payment_method = intent.get("payment_method", "unknown")
            payment.save()

            return Response({
                "status": payment.status,
                "amount": payment.amount,
                "currency": payment.currency,
                "created": payment.created_at,
                "payment_method": payment.payment_method,
                "refund_status": payment.refund_status,
                "subscription_id": payment.subscription_id,
                "product_id": payment.product_id,
                "client_secret": payment.client_secret
            }, status=status.HTTP_200_OK)
        
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.InvalidRequestError:
            return Response({"error": "Invalid Payment Intent ID"}, status=status.HTTP_400_BAD_REQUEST)

class RefundPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_intent_id):
        try:
            # Check if payment exists
            payment = Payment.objects.get(payment_intent_id=payment_intent_id)

            # Verify payment was successful before refunding
            if payment.status != "succeeded":
                return Response({"error": "Payment was not successful, cannot refund"}, status=400)

            # Process refund
            refund = stripe.Refund.create(payment_intent=payment_intent_id)

            # Update database
            payment.refund_status = "refunded"
            payment.save()

            return Response({"message": "Payment refunded successfully"}, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

        except stripe.error.InvalidRequestError:
            return Response({"error": "Invalid payment intent ID"}, status=status.HTTP_400_BAD_REQUEST)


class UsageTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        month = request.data.get("month", datetime.today().strftime("%Y-%m-01"))
        
        # Check for existing record
        existing_record = UsageTracking.objects.filter(user=request.user, month=month).first()
        
        if existing_record:
            existing_record.videos_analyzed += 1
            existing_record.save()
            return Response({"message": "Usage updated", "data": UsageTrackingSerializer(existing_record).data})

        serializer = UsageTrackingSerializer(data={"user": request.user.id, "month": month, "videos_analyzed": 1})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class MyPaymentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

class CheckVideoLimitView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            subscription = UserSubscription.objects.filter(user=user, is_active=True).last()
            if not subscription:
                return Response({"error": "No active subscription"}, status=404)

            plan_limit = subscription.plan.video_analysis_limit
            usage = UsageTracking.objects.filter(user=user, month=datetime.today().replace(day=1)).first()
            current_usage = usage.videos_analyzed if usage else 0

            if plan_limit is None:
                return Response({"status": "unlimited", "videos_used": current_usage})
            elif current_usage >= plan_limit:
                return Response({"status": "limit_reached", "limit": plan_limit, "videos_used": current_usage})
            else:
                return Response({"status": "allowed", "limit": plan_limit, "videos_used": current_usage})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# forgot password

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.core.mail import send_mail
# from django.contrib.auth import get_user_model
# from .serializers import ForgotPasswordSerializer
# from .models import PasswordResetToken
# import random
# import string

# class ForgotPasswordView(APIView):
#     def post(self, request):
#         serializer = ForgotPasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try:
#                 # Check if the user exists using get_user_model()
#                 user = get_user_model().objects.get(email=email)

#                 # Generate a random password reset token
#                 token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

#                 # Save the token to the PasswordResetToken model
#                 PasswordResetToken.objects.create(user=user, token=token)

#                 # Send email with the token link (you should configure an email backend)
#                 reset_link = f"http://127.0.0.1:8000/reset-password/{token}/"

#                 send_mail(
#                     'Password Reset Request',
#                     f'Click the link to reset your password: {reset_link}',
#                     'no-reply@yourdomain.com',
#                     [email],
#                     fail_silently=False,
#                 )

#                 return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

#             except get_user_model().DoesNotExist:
#                 return Response({"error": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import PasswordResetForm
# from .models import PasswordResetToken
# from django.contrib.auth import update_session_auth_hash

# class ResetPasswordView(APIView):
#     def get(self, request, token):
#         try:
#             # Validate the token
#             reset_token = PasswordResetToken.objects.get(token=token)

#             # Check if the token is valid, if expired or used, redirect accordingly.
#             # Here, we assume the token is valid if it's in the DB (you can add expiration logic if needed)
#             user = reset_token.user

#             # Pass the user object to the template to display a password reset form
#             return render(request, 'reset_password.html', {'token': token, 'user': user})

#         except PasswordResetToken.DoesNotExist:
#             return HttpResponse("Invalid token or token expired.")

#     def post(self, request, token):
#         try:
#             # Find the token
#             reset_token = PasswordResetToken.objects.get(token=token)

#             # Get user from the token
#             user = reset_token.user

#             # Ensure the user submits a valid password (you can use Django's PasswordChangeForm here)
#             password = request.data.get('password')  # This can come from a form

#             # Set the new password for the user
#             user.set_password(password)
#             user.save()

#             # Delete the reset token to prevent re-use
#             reset_token.delete()

#             return HttpResponse("Password has been successfully reset.")

#         except PasswordResetToken.DoesNotExist:
#             return HttpResponse("Invalid token or token expired.")


from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import PasswordResetOTP
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer

User = get_user_model()

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Generate OTP and store it
            generated_otp = PasswordResetOTP.generate_otp()
            PasswordResetOTP.objects.create(user=user, otp=generated_otp)

            # Send OTP to email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is {generated_otp}.",
                "your-email@gmail.com",
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                otp_record = PasswordResetOTP.objects.filter(
                    user=user, otp=otp, created_at__gte=now() - timedelta(minutes=10)
                ).first()

                if otp_record:
                    user.set_password(new_password)
                    user.save()
                    otp_record.delete()  # Delete OTP after use
                    return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# render url:-
# https://dashboard.render.com/web/srv-cv5us27noe9s73boee10/deploys/dep-cv61thvnoe9s73bppn20