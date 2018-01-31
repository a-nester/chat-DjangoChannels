from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class Rooms(models.Model):
    title = models.CharField(max_length = 200)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def format_response(self):
        response = {
            'message' : str(self.message),
            'username' : str(self.user.username),            
        }
        return response