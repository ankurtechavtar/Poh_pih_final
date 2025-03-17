
from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import get_user_model
User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  

    class Meta:
        model = User  
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']  # Set username as email
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return User.objects.create(**validated_data)



from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": ["Invalid email"]})

        # Check password
        if not check_password(password, user.password):
            raise serializers.ValidationError({"password": ["Invalid password"]})

        return user



from .models import DanceLevel,Interest,Style,UserInterest,CustomUser

class DanceLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanceLevel
        fields = '__all__'

class IntersetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'




# class UserInterestSerializer(serializers.ModelSerializer):
#     user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user') 
#     interest_ids = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True, source='interests') 

#     class Meta:
#         model = UserInterest
#         fields = ['id', 'user_id', 'interest_ids']

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Interest

User = get_user_model()  # Dynamically get the custom user model

class UserInterestSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    interest_ids = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True, source='interests')

    class Meta:
        model = UserInterest  # Assuming UserInterest model has user and interests fields
        fields = ['id', 'user_id', 'interest_ids']

# Profile management related serialziers

class UserProfileSerializer(serializers.ModelSerializer):
    dance_level = DanceLevelSerializer(read_only=True)
    interests = IntersetSerializer(many=True, read_only=True)
    styles = StyleSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture', 'dance_level', 'interests', 'styles']

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_picture', 'dance_level', 'interests', 'styles']
        extra_kwargs = {'interests': {'required': False}, 'styles': {'required': False}}

class UploadProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# payment and subscription related serializers 

from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, Payment, UsageTracking

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UsageTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageTracking
        fields = '__all__'

