from django.db import models
import django
import array

# Create your models here.

class Voiceprint(models.Model):
    username = models.CharField(max_length=100, unique=True)
    voiceprint = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
