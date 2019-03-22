from django.test import TestCase
from rest_framework.test import RequestsClient
from apps.accounts.models import UserProfile


class UserTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_user_success(self):
        client = RequestsClient()
        response = client.post(
            "http://testserver/api/v1/user/",
            json={
                "username": "james",
                "given_name": "James",
                "family_name": "Kirk",
                "gender": "M",
                "password": "tree garden jump fox",
                "birthdate": "1952-01-03",
                "nickname": "Jim",
                "phone_number": "+15182345678",
                "email": "jamess@example.com",
             })
        self.assertEqual(response.status_code, 201, response.text)
        self.assertDictEqual(response.json(), {
            "iss": "https://alpha.verifymyidentity.com",
            "subject": "123456789012345", 
            "username": "james",
            "given_name": "James",
            "family_name": "Kirk",
            "name": "James Kirk",
            "gender": "male",
            "birthdate": "1952-01-03",
            "nickname": "Jim",
            "phone_number": "+15182345678",
            "email": "jamess@example.com",
            "ial": 1,
            "id_assursance" : [],
            "document" : [],
            "address": []
        })

        up = UserProfile.objects.get(sub=response.json()['subject'])
        self.assertEqual(up.user.username, "bob")
