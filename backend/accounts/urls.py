from django.urls import path, include
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('email/',views.check_email),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('token/',obtain_jwt_token),
    path('token/refresh/',refresh_jwt_token),
    path('token/verify/',verify_jwt_token),
   
]