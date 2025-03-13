from django.shortcuts import render
# from django.http import httpResponse
from django.views import View 

class HomeView(View):
    def get(self,request):
        return render(request,'home.html')



from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import SignupSerializer

User = get_user_model()  # Get the custom user model

class SignupListView(generics.ListAPIView):
    queryset = User.objects.all()  # Now it correctly references CustomUser
    serializer_class = SignupSerializer

class SignupCreateView(generics.CreateAPIView):  
    queryset = User.objects.all()  
    serializer_class = SignupSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

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
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import generics
from .models import DanceLevel, Interest, Style
from .serializers import DanceLevelSerializer, IntersetSerializer, StyleSerializer

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



from .models import UserInterest
from .serializers import UserInterestSerializer


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

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from .models import CustomUser
from .serializers import (
    UserProfileSerializer, UpdateUserProfileSerializer,
    UploadProfilePictureSerializer, ChangePasswordSerializer
)


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


class UploadProfilePictureView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UploadProfilePictureSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = "id"


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



import requests
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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


# render url:-
# https://dashboard.render.com/web/srv-cv5us27noe9s73boee10/deploys/dep-cv61thvnoe9s73bppn20