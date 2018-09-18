from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.urls import reverse
from oauth2_provider import scopes
from .settings import oidc_settings

Scopes = scopes.get_scopes_backend()


class Wellknown(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):

        return Response({
            "issuer": oidc_settings.OIDC_ISSUER,
            "authorization_endpoint": oidc_settings.OIDC_ISSUER + reverse("oauth2_provider:authorize"),
            "token_endpoint": oidc_settings.OIDC_ISSUER + reverse("oauth2_provider:token"),
            "revocation_endpoint": oidc_settings.OIDC_ISSUER + reverse("oauth2_provider:revoke-token"),
            "response_types_supported": [
                "code",
                "token",
                "id_token",
                "code token",
                "code id_token",
                "token id_token",
                "code token id_token",
                "none",
            ],
            "scopes_supported": Scopes.get_all_scopes().keys(),
            "claims_supported": [],
        })
