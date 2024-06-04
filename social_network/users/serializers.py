from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from .models import Avatar

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)

class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_staff', 'is_active', 'date_joined')

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['image', 'current']

    def create(self, validated_data):
        user = self.context['request'].user
        Avatar.objects.filter(user=user, current=True).update(current=False)
        return Avatar.objects.create(user=user, **validated_data)
    
class CurrentAvatarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ['image']