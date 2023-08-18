from django.db.migrations import serializer
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PhoneNumberApp.models import CustomUser
from api.serializers import CustomUserSerializer


@csrf_exempt
def number_list(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        user = CustomUser.objects.get(pk=pk)
        invited_persons = user.custom_user.all().values('phone_number')
        serializer = CustomUserSerializer(invited_persons, many=True)
        return JsonResponse(serializer.data, safe=False)