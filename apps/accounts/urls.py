from django.urls import path

from accounts.views import UserProfileView


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]