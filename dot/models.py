from django.db import models

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="", null=True, blank=True,default="")
