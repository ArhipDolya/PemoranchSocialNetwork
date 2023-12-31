from django.db import models
from django.conf import settings

import random


class PemoranLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pemoran = models.ForeignKey("Pemoran", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Pemoran(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='pemoran_user', blank=True, through=PemoranLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content

    @property
    def is_repemo(self):
        return self.parent != None
    
