from django.db import models
from django.db.models import CharField, TextField, BooleanField, DateTimeField
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = CharField(max_length=127)
    memo = TextField(blank=True)
    created = DateTimeField(auto_now_add=True)
    important = BooleanField(default=False)
    date_completion = DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
