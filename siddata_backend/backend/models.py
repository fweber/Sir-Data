from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
import uuid
import base64
from siddata_backend import settings
import datetime


class X5gonResource(models.Model):

    id= models.AutoField(primary_key=True,editable=False)
    x5gon_id = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    language = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    keywords = ArrayField(models.CharField(max_length=512), null=True)
    concepts = ArrayField(models.CharField(max_length=512), null=True)
    description = models.CharField(max_length=2048, null=True, default="...")

class X5gonUser(models.Model):

    id = models.AutoField(primary_key=True,editable=False)
    x5gon_id = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024, default=None, null=True)
    country = models.CharField(max_length=1024, default=None, null=True)
    interests = models.CharField(max_length=1024, default=None, null=True)

    def get_properties(self,id):
        me = models.User.objects.get(id=1)
        properties = {
            "id":self.id,
            "x5gon_id":self.x5gon_id,
            "name":self.name,
            "country":self.country,
            "interests":self.interests,
        }

        return properties


class UserResource(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(X5gonUser, on_delete=models.CASCADE)
    resource = models.ForeignKey(X5gonResource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    crown = models.BooleanField(default=False)
    expert_on = models.BooleanField(default=False)

class Interests(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=1024)

class Question(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    resource = models.ForeignKey(X5gonResource, on_delete=models.CASCADE)
    question = models.CharField(max_length=1024)
    correct_answer = models.CharField(max_length=1024)

class QuestionUser(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(X5gonUser, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1024)

class ChatHistory(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    sender = models.ForeignKey(X5gonUser, on_delete=models.CASCADE, related_name = "sender")
    receiver = models.ForeignKey(X5gonUser, on_delete=models.CASCADE, related_name = "receiver")
    message = models.CharField(max_length=1024)

