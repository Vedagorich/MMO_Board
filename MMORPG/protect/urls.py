from django.urls import path, include
from .views import RegisterUser, LoginUser, LogoutUser, RegisterUserCode, check_code

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('register/code/', check_code, name='code'),
    path('login/', LoginUser.as_view(template_name='protect/login.html'), name='login'),
    path('logout/', LogoutUser, name='logout'),
    ]