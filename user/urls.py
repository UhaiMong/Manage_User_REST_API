from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'list', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view(),name='register'),
    path('login/', views.UserLoginApiView.as_view(),name='login'),
    path('logout/', views.UserLogoutApiView.as_view(),name='logout'),
    path('profile_update/', views.ProfileUpdateApiView.as_view(),name='profile_update'),
]