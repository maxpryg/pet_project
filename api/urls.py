from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('comments/', views.CommentCreate.as_view(), name='comments'),
    path('posts/', views.PostViewSet.as_view(), name='posts'),
    path('authors/', views.AuthorViewSet.as_view({'get': 'list'}), name='authors_list'),
    path('authors/<int:pk>/', views.AuthorViewSet.as_view({'get': 'retrieve'}),
         name='authors_detail'),
]
