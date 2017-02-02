from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=120, blank=False)
  description = models.TextField(blank=False)
  completed = models.BooleanField(default=False)
  owner = models.ForeignKey('auth.User', related_name='todos', on_delete=models.CASCADE)

  class Meta:
    ordering = ('created',)
