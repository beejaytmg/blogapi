from django.urls import path
from .views import UserLoginView, UserRegisterView, BlogPostCreateView, BlogListView, BlogPostView
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserRegisterView.as_view(), name='user_signup'),
    path('blogs', BlogListView.as_view(), name='list-blog'),
    path('blog/create', BlogPostCreateView.as_view(), name='create-blog'),
    path('blog/<slug:slug>/', BlogPostView.as_view(), name='blog-detail'),
]