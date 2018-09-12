import jwt
from django.conf import settings
from .settings import oidc_settings


def get_jwt_builder():
    return oidc_settings.OIDC_JWT_BUILDER


class DefaultBuilder(object):
    def encode(self, claims):
        return jwt.encode(
            claims,
            settings.SECRET_KEY,
            algorithm='HS256').decode("utf-8")

    def decode(self, token, *args, **kwargs):
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithm='HS256',
            **kwargs)
