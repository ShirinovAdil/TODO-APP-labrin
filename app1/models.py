from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    goal = models.CharField(max_length=150, verbose_name="Goal")
    description = models.TextField(verbose_name="Task description")
    created_date = models.DateTimeField()
    end_date = models.DateTimeField()
    by_who = models.CharField(max_length=150, verbose_name="Created by")
    viewable_by = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.goal
