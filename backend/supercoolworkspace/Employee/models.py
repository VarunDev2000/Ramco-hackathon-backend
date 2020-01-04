from django.db import models
from django import forms
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django import forms


class Employee(models.Model):
    #ip = models.CharField(max_length=500, null=False)
    #name = models.CharField(max_length=500, null=False)
    Angry = models.IntegerField(null = False)
    Disgusted = models.IntegerField(null = False)
    Happy = models.IntegerField(null = False)
    Neutral = models.IntegerField(null = False)
    Sad = models.IntegerField(null = False)
    Timestamp = models.DateField(default = None)


    class Meta:
        verbose_name_plural = "Employee Details"

    #def __str__(self):
        #return self.name
