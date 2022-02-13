from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name="team name",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="team user",
    )

