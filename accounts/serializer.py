from django.contrib.auth import get_user_model


from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Role

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'status', 'role_details')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        users = User.objects.filter(status='active')
        if users.filter(username=username).exists():
            raise serializers.ValidationError('username already exists')
        if users.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        user = User.objects.create(
            username=username, email=email
        )
        user.set_password(password)
        user.roles.add(3)
        user.save()
        Token.objects.create(user=user)
        return user
    
    def get_role_details(self, obj):
        return list(obj.roles.all().values_list("role_name", flat=True))