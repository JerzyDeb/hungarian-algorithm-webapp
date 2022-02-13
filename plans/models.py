from django.contrib.auth.models import User
from django.db import models

from teams.models import Team


class Plan(models.Model):
    createdDate = models.DateTimeField(
        verbose_name="create date",
    )
    name = models.CharField(
        max_length=64,
        verbose_name="plan name",
    )
    pdf = models.FileField(
        upload_to='plans',
        verbose_name="plan pdf",
    )
    method = models.CharField(
        max_length=2,
        verbose_name="method name",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="plan user",
    )
    team = models.CharField(
        max_length=64,
        verbose_name="team name",
    )
