from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.urls import reverse
from oauth2_provider import scopes
from oauth2_provider.settings import oauth2_settings
from .settings import oidc_settings
from .claims import get_claims_provider
from .jwt import get_jwt_builder

Scopes = scopes.get_scopes_backend()
ClaimsProvider = get_claims_provider()

class Wellknown(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):

        return Response({
            "grant_types_supported": [
                "authorization_code",
                "implicit",
                "refresh_token",
            ],
            "issuer": oidc_settings.OIDC_ISSUER,
            "authorization_endpoint": oidc_settings.OIDC_ISSUER + reverse("oauth2_provider:authorize"),
            "token_endpoint": oidc_settings.OIDC_ISSUER + reverse("oauth2_provider:token"),
            "revocation_endpoint": oidc_settings.OIDC_ISSUER + reverse("oauth2_provider:revoke-token"),
            "response_types_supported": oauth2_settings.OAUTH2_SERVER_CLASS.get_all_response_types(),
            "scopes_supported": Scopes.get_all_scopes().keys(),
            "claims_supported": ClaimsProvider.get_supported_claims(),
            "jwks_uri": oidc_settings.OIDC_ISSUER + reverse("jwks_uri"),
        })


class JWKSURI(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        return Response({
            "keys": [get_jwt_builder().get_jwks()]})
