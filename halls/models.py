from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hall(models.Model):
    title = models.CharField(max_length = 100)
    user  = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.title
class Video(models.Model):
    title = models.CharField(max_length = 100)
    url = models.URLField()
    youtube_id = models.CharField(max_length = 500)
    hall = models.ForeignKey(Hall,on_delete = models.CASCADE)
    def __str__(self):
        return self.title
