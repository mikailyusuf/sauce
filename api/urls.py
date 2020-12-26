from django.urls import path

from api.views import UserRegistration

urlpatterns = [
    path('',UserRegistration.as_view()),

]