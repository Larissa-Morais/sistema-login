from django.db import models
from uuid import uuid4

class User(models.Model):
    id_user = models.UUIDField(primary_key=True, default=uuid4)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
