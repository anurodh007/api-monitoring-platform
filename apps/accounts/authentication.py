from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework import authentication, exceptions

User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        # Get authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        # Format: "Bearer <id_token>"
        try:
            id_token = auth_header.split(' ').pop()
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid token format.')

        # Verify the token id against Firebase
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid Firebase token: {str(e)}')

        # Extract data from token
        uid = decoded_token.get('uid')

        if not uid:
            raise exceptions.AuthenticationFailed('Firebase token missing UID.')

        email = decoded_token.get('email')
        picture = decoded_token.get('picture', '')

        user, created = User.objects.get_or_create(
            username=uid,
            defaults={
                'email': email if email else '',
                'profile_pic_url': picture
            }
        )

        if not created:
            if picture and user.profile_pic_url != picture:
                user.profile_pic_url = picture
                user.save()

        return (user, None)