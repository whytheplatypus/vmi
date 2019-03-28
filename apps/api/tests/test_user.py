from datetime import timedelta, date
from django.utils import timezone
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.test import RequestsClient
from oauth2_provider.models import get_application_model, get_access_token_model
from oauth2_provider.settings import oauth2_settings
from apps.accounts.models import UserProfile

User = get_user_model()
Application = get_application_model()
AccessToken = get_access_token_model()


class UserTestCase(TestCase):
    maxDiff = None

    def get_username(self):
        return "bob"

    def get_password(self):
        return "fubar"

    def get_permissions(self):
        return Permission.objects.filter(
            content_type=ContentType.objects.get_by_natural_key('accounts', 'userprofile'),
        ).all()

    def get_user(self):
        user = User.objects.create(
            username=self.get_username(),
            password=self.get_password(),
        )
        for permission in self.get_permissions():
            user.user_permissions.add(permission)
        return User.objects.get(pk=user.pk)

    def get_expires(self):
        return timezone.now() + timedelta(
            seconds=oauth2_settings.AUTHORIZATION_CODE_EXPIRE_SECONDS)

    def get_client(self):
        return Application.objects.create(
            name="test",
        )

    def setUp(self):
        self.token = AccessToken.objects.create(
            user=self.get_user(),
            application=self.get_client(),
            expires=self.get_expires(),
            token="test",
        )

    def test_create_user_success(self):
        client = RequestsClient()
        response = client.post(
            "http://testserver/api/v1/user/",
            json={
                "preferred_username": "james",
                "given_name": "James",
                "family_name": "Kirk",
                "gender": "M",
                "password": "tree garden jump fox",
                "birthdate": "1952-01-03",
                "nickname": "Jim",
                "phone_number": "+15182345678",
                "email": "jamess@example.com",
            },
            headers={
                'Authorization': "Bearer {}".format(self.token.token),
            })
        self.assertEqual(response.status_code, 201, response.text)
        self.assertDictContainsSubset({
            "iss": "http://localhost",
            # "subject": "123456789012345",
            "preferred_username": "james",
            "given_name": "James",
            "family_name": "Kirk",
            "name": "James Kirk",
            "gender": "male",
            "birthdate": "1952-01-03",
            "nickname": "Jim",
            "phone_number": "+15182345678",
            "email": "jamess@example.com",
            "ial": '1',
            # "id_assursance": [],
            "document": [],
            "address": []
        }, response.json())

        up = UserProfile.objects.get(subject=response.json()['sub'])
        self.assertEqual(up.user.username, "james")

    def test_read_user_success(self):
        client = RequestsClient()
        create_response = client.post(
            "http://testserver/api/v1/user/",
            json={
                "preferred_username": "james",
                "given_name": "James",
                "family_name": "Kirk",
                "gender": "M",
                "password": "tree garden jump fox",
                "birthdate": "1952-01-03",
                "nickname": "Jim",
                "phone_number": "+15182345678",
                "email": "jamess@example.com",
            },
            headers={
                'Authorization': "Bearer {}".format(self.token.token),
            })
        response = client.get(
             "http://testserver/api/v1/user/{}/".format(create_response.json()['sub']), headers={
                'Authorization': "Bearer {}".format(self.token.token),
             })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertDictContainsSubset({
            "iss": "http://localhost",
            # "subject": "123456789012345",
            "preferred_username": "james",
            "given_name": "James",
            "family_name": "Kirk",
            "name": "James Kirk",
            "gender": "male",
            "birthdate": "1952-01-03",
            "nickname": "Jim",
            "phone_number": "+15182345678",
            "email": "jamess@example.com",
            "ial": '1',
            # "id_assursance": [],
            "document": [],
            "address": []
        }, response.json())

    def test_update_user_success(self):
        self.maxDiff = None
        client = RequestsClient()
        response = client.post(
            "http://testserver/api/v1/user/",
            json={
                "preferred_username": "james",
                "given_name": "James",
                "family_name": "Kirk",
                "gender": "M",
                "password": "tree garden jump fox",
                "birthdate": "1952-01-03",
                "nickname": "Jim",
                "phone_number": "+15182345678",
                "email": "jamess@example.com",
            },
            headers={
                'Authorization': "Bearer {}".format(self.token.token),
            })
        update_response = client.put(
             "http://testserver/api/v1/user/{}/".format(response.json()['sub']),
             json={
                "birthdate": "2233-03-22",
                "family_name": "bob",
             }, headers={
                'Authorization': "Bearer {}".format(self.token.token),
             })
        self.assertEqual(update_response.status_code, 200, update_response.text)
        self.assertEqual("2233-03-22", update_response.json()['birthdate'])

        up = UserProfile.objects.get(subject=response.json()['sub'])
        self.assertEqual(up.birth_date, date(2233, 3, 22))
        self.assertEqual(up.user.last_name, "bob")

    def test_delete_user_success(self):
        self.maxDiff = None
        client = RequestsClient()
        response = client.post(
            "http://testserver/api/v1/user/",
            json={
                "preferred_username": "james",
                "given_name": "James",
                "family_name": "Kirk",
                "gender": "M",
                "password": "tree garden jump fox",
                "birthdate": "1952-01-03",
                "nickname": "Jim",
                "phone_number": "+15182345678",
                "email": "jamess@example.com",
            },
            headers={
                'Authorization': "Bearer {}".format(self.token.token),
            })

        delete_response = client.delete(
             "http://testserver/api/v1/user/{}/".format(response.json()['sub']), headers={
                'Authorization': "Bearer {}".format(self.token.token),
             })
        self.assertEqual(delete_response.status_code, 204, delete_response.text)
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(subject=response.json()['sub'])
