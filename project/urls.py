from datacenter.active_passcards_view import active_passcards_view
from datacenter.passcard_info_view import passcard_info_view
from datacenter.storage_information_view import storage_information_view
from django.urls import path

urlpatterns = [
    path('', active_passcards_view, name='active_passcards'),
    path('storage_information', storage_information_view, name='storage_information'),
    path('passcard_info/<uuid:passcode>', passcard_info_view, name='passcard_info'),
]
