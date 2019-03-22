from rest_framework import serializers, viewsets
from django.contrib.auth import get_user_model
from apps.accounts.models import (
    UserProfile,
    GENDER_CHOICES,
)
# {
#     "username": "james",
#     "given_name": "James",
#     "family_name": "Kirk",
#     "gender": "male",
#     "password": "tree garden jump fox",
#     "birthdate": "1952-01-03",
#     "nickname": "Jim",
#     "phone_number": "+15182345678",
#     "email": "jamess@example.com"
# }
User = get_user_model()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, source='user.username')
    given_name = serializers.CharField(max_length=255, source='user.first_name')
    family_name = serializers.CharField(max_length=255, source='user.last_name')
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    password = serializers.CharField(max_length=255, write_only=True, source='user.password')
    birthdate = serializers.DateField()
    nickname = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255, source='user.email')
    phone_number = serializers.CharField(max_length=255)

    def create(self, validated_data):
        # raise Exception(validated_data)
        user_data = validated_data.get('user', {})
        user = User.objects.create(**user_data)

        return UserProfile.objects.create(
            nickname=validated_data.get('nickname'),
            gender_identity=validated_data.get('gender'),
            mobile_phone_number=validated_data.get('phone_number'),
            user=user,
        )

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname')
        instance.gender_identity = validated_data.get('gender')
        instance.mobile_phone_number = validated_data.get('phone_number')
        instance.save()

        user_data = validated_data.get('user', {})

        instance.user.username = user_data.get('requested_username')
        instance.user.first_name = user_data.get('first_name')
        instance.user.last_name = user_data.get('last_name')
        instance.user.email = user_data.get('email')
        instance.user.save()


class UserViewSet(viewsets.ModelViewSet):
     lookup_field = "sub"
     queryset = UserProfile.objects.all()
     serializer_class = UserSerializer

     # def create(self, request, *args, **kwargs):
     #     pass
     # def list(self, request, *args, **kwargs):
     #     pass
     # def retrieve(self, request, *args, **kwargs):
     #     pass
     # def update(self, request, *args, **kwargs):
     #     pass
     # def destroy(self, request, *args, **kwargs):
     #     pass
