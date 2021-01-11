from django.urls import path

from authentication.views import RegisterView, VerifyEmail, LogoutAPIView, LoginAPIView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

]
