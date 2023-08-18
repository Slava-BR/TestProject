from django import forms
from phonenumber_field.formfields import PhoneNumberField


class PhoneForm(forms.Form):
    number = PhoneNumberField(region='RU')


class CodeForm(forms.Form):
    code = forms.CharField(max_length=4, min_length=4)


class InviteCode(forms.Form):
    code = forms.CharField(max_length=6, min_length=6)