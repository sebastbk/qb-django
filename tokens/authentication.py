from rest_framework import authentication

from .models import Token


class APITokenAuthentication(authentication.TokenAuthentication):
    model = Token
