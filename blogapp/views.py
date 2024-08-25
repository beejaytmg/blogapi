from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSerializer, BlogPostSerializer, BlogListSerializer
from rest_framework import generics, permissions, exceptions, serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import BlogPost
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

   
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=400)
class BlogPostCreateView(generics.CreateAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
class BlogListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        blogs = BlogPost.objects.all()
        serializer = BlogListSerializer(blogs, many=True)
        return Response(serializer.data)
class BlogPostView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]