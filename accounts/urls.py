from django.urls import path

from accounts import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('login/', views.CustomLoginView.as_view()),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(),
         name="activate"),
    path('check-email/', views.CheckEmailView.as_view(), name="check_email"),
    path('success/', views.SuccessView.as_view(), name="success"),
]
