from django.test import TestCase
from rest_framework.test import RequestsClient


class UserTestCase(TestCase):
    maxDiff = None

    def setUp(self):
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
        self.subject = response.json()['sub']

    def test_create_identifier_success(self):
        client = RequestsClient()
        response = client.post(
            "http://testserver/api/v1/user/{}/identifier/".format(self.subject),
            json={
                "description": "NY Medicaid card.",
                "classification": "ONE-SUPERIOR-OR-STRONG+",
                "exp": "2022-01-01",
                "note": "A paper copy of the document is on file.",
                "verification_date": "2019-03-04"
            })

        self.assertEqual(201, response.status_code, response.text)

        self.assertDictContainsSubset({
            "description": "NY Medicaid card.",
            "classification": "ONE-SUPERIOR-OR-STRONG+",
            "exp": "2022-01-01",
            "verifier_subject": "876545671054321",
            "note": "A paper copy of the document is on file.",
            "verification_date": "2019-03-04"
        }, response.json(), response.json())
