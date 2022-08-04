from django.urls import path

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api import views

router = routers.SimpleRouter()
router.register(r'authors', views.AuthorViewSet, basename='authors')
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('subscribe/', views.SubscriberCreate.as_view(),
         name='subscriber_create'),
    path('main_image/', views.ImageCreate.as_view(),
         name='main_image_create'),
    path('profile/', views.AuthorProfileUpdate.as_view(), name='profile'),
]

urlpatterns += router.urls
