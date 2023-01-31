from django.utils.timezone import localtime
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    non_closed_visits = [
        {
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at),
            'duration': visit.get_duration(),
            'is_strange': visit.is_strange()
        }
        for visit in Visit.objects.filter(leaved_at=None)
    ]
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
