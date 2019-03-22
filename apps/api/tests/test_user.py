import requests
from django.test import TestCase

class UserTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_user_success(self):
        response = requests.post(
            "http://testserver/api/v1/user/",
            json={
                "username": "james",
                "given_name": "James",
                "family_name": "Kirk",
                "gender": "male",
                "password": "tree garden jump fox",
                "birthdate": "1952-01-03",
                "nickname": "Jim",
                "phone_number": "+15182345678",
                "email": "jamess@example.com",
             })
        user = User.objects.get(sub=response.subject)
        self.assertEqual(user.username, "james")
