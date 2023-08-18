
from django.urls import path

from api.views import number_list

urlpatterns = [path('profile/<int:pk>/',  number_list, name=' number_list'),]
