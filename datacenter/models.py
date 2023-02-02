from django.db import models
from django.utils.datetime_safe import datetime
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

    def get_duration(self) -> str:
        if not self.leaved_at:
            time_range = localtime() - self.entered_at
        else:
            time_range = self.leaved_at - self.entered_at
        hours, seconds = divmod(time_range.total_seconds(), 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"

    def is_strange(self) -> bool:
        end_time = localtime() if not self.leaved_at else self.leaved_at
        return (end_time - self.entered_at).total_seconds() > 3600
