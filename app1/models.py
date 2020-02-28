from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    goal = models.CharField(max_length=150, verbose_name="Goal")
    description = models.TextField(verbose_name="Task description")
    created_date = models.DateTimeField()
    end_date = models.DateTimeField()
    by_who = models.CharField(max_length=150, verbose_name="Created by")
    viewable_by = models.ManyToManyField(User, related_name="viewable_by")
    editable_by = models.ManyToManyField(User, related_name="editable_by")

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.goal


class Comment(models.Model):
    comment_sender = models.CharField(verbose_name="Comment author", max_length=250)
    comment_text = models.CharField(verbose_name="Comment text", max_length=250)
    comment_date = models.DateTimeField(default=timezone.now)
    comment_related_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_sender + ' - ' + self.comment_text
