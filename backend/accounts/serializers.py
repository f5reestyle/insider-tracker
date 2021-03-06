from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from selenium import webdriver

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   email=validated_data['email'],
                                   api_key=validated_data['api_key'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    def validate_password(self, value):
        try:
            validators.validate_password(password=value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    class Meta:
        model = User
        fields = ['pk','username','password','telegram_id','email','api_key']


