from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from PhoneNumberApp.models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region="RU")

