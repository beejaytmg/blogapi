from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from .models import BlogPost
class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', 'password', 'access_token', 'refresh_token')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    def get_access_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
class BlogListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'url')

    def get_url(self, obj):
        return f"https://bijayakumartamang.com.np/post/{obj.slug}"


