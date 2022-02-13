from django.contrib.auth.models import User
from django.db import models

from plans.models import Plan
from teams.models import Team


class Worker(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name="worker name",
    )
    surname = models.CharField(
        max_length=64,
        verbose_name="worker surname",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name="worker team",
    )


class Task(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name="task name",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name="task team",
    )


class Execution(models.Model):
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        verbose_name="worker which executes task"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="task which is executing"
    )
    time = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name="price/time of execution"
    )
