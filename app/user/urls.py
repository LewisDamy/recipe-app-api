"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# used for the reverse function to find defined at test_user_api.py line 11
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateUserView.as_view(), name='token')
]
