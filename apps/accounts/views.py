from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserProfileSerializer


"""
API View to retrieve and update current user
"""
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user