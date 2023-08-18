from django.test import TestCase
from PhoneNumberApp.models import CustomUser, authenticate


# Create your tests here.
class AuthenticateTestCase(TestCase):

    def test_authenticate_correct_number(self):
        user = CustomUser.objects.create(phone_number='+78005553535', invite_code='GFJ32J')
        self.assertEqual(authenticate(user.phone_number), user)

    def test_authenticate_uncorrected_number(self):
        self.assertEqual(authenticate('+78005553535'), None)

