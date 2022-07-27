from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('login/', views.CustomLoginView.as_view()),
    path('profile/<int:pk>', views.ProfileView.as_view(), name="profile"),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(),
         name="activate"),
    path('check-email/', views.CheckEmailView.as_view(), name="check_email"),
    path('success/', views.SuccessView.as_view(), name="success"),
]
