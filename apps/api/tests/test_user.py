import datetime
from django.test import TestCase
from rest_framework.test import RequestsClient
from apps.accounts.models import UserProfile


class UserTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        pass

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
             })
        response = client.get(
             "http://testserver/api/v1/user/{}/".format(create_response.json()['sub']))
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
             })
        update_response = client.put(
             "http://testserver/api/v1/user/{}/".format(response.json()['sub']),
             json={
                "birthdate": "2233-03-22",
                "family_name": "bob",
             })
        self.assertEqual(update_response.status_code, 200, update_response.text)
        self.assertEqual("2233-03-22", update_response.json()['birthdate'])

        up = UserProfile.objects.get(subject=response.json()['sub'])
        self.assertEqual(up.birth_date,  datetime.date(2233, 3, 22))
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
             })
        delete_response = client.delete(
             "http://testserver/api/v1/user/{}/".format(response.json()['sub']))
        self.assertEqual(delete_response.status_code, 204, delete_response.text)
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(subject=response.json()['sub'])
