from django.urls import path
from django.conf.urls import url
from .views import CreateUserAPIView, LoginUser

urlpatterns = [
    path('user/register/', CreateUserAPIView.as_view()),
    path('user/login/', LoginUser.as_view())
]