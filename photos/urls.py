from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreateView, LoginView, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]

