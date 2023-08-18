from PhoneNumberApp.views import authorization, activate_code, profile, logout
from django.urls import path

urlpatterns = [path('authorization/', authorization, name='authorization'),
               path('activate/', activate_code, name='activate'),
               path('profile/', profile, name='profile'),
               path('logout/', logout, name='logout')
               ]
