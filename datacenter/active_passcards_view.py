from datacenter.models import Passcard
from django.shortcuts import render


def active_passcards_view(request):
    active_passcards = Passcard.objects.filter(is_active=True)
    context = {
        'active_passcards': active_passcards,
    }
    return render(request, 'active_passcards.html', context)
