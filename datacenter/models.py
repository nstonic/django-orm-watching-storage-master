from datetime import timedelta

from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def _get_duration(self) -> timedelta:
        print(type(localtime(self.leaved_at) - localtime(self.entered_at)))
        return localtime(self.leaved_at) - localtime(self.entered_at)

    def output_duration(self) -> str:
        time_range = self._get_duration()
        hours, seconds = divmod(time_range.total_seconds(), 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"

    def is_strange(self) -> bool:
        time_range = self._get_duration()
        return time_range.total_seconds() > 3600
