from django.urls import path

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api import views

router = routers.SimpleRouter()
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('comments/', views.CommentCreate.as_view(), name='comment_create'),
    path('posts/', views.PostViewSet.as_view(), name='posts'),
    path('subscribe/', views.SubscriberCreate.as_view(),
         name='subscriber_create'),
    path('main_images/', views.MainImageCreate.as_view(),
         name='main_image_create'),
    path('additional_images/', views.AdditionalImageCreate.as_view(),
         name='additional_images'),
    path('profile/', views.AuthorProfileUpdate.as_view(), name='comments'),
]

urlpatterns += router.urls
