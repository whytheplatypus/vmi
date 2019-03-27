from apps.ial.models import (
    IdentityAssuranceLevelDocumentation,
    EVIDENCE_CLASSIFICATIONS)

from rest_framework import serializers, viewsets
from django.contrib.auth import get_user_model
User = get_user_model()

# {
# "description": "NY Medicaid card.",
# "classification": "ONE-SUPERIOR-OR-STRONG+",
# "exp": "2022-01-01",
# "verifier_subject": "876545671054321",
# "note": "A paper copy of the document is on file.",
# "verification_date": "2019-03-04"
# }


class IdentifierSerializer(serializers.ModelSerializer):
    classification = serializers.ChoiceField(source="evidence", choices=EVIDENCE_CLASSIFICATIONS)
    description = serializers.CharField(source="id_verify_description")
    exp = serializers.DateField(source='expires_at')

    class Meta:
        model = IdentityAssuranceLevelDocumentation


class IdentifierViewSet(viewsets.ModelViewSet):
    serializer_class = IdentifierSerializer

    def get_queryset(self):
        IdentityAssuranceLevelDocumentation.objects.all(subject_user=self.kwargs['user_subject'])

    def create(self, request, *args, **kwargs):
        request.data['subject_user'] = User.objects.get(userprofile__subject=self.kwargs['user_subject']).pk
        return super().create(request, *args, **kwargs)
