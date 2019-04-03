from django.contrib.auth.models import User
from django.db import models


class NodeBBUserRelation(models.Model):
    edx_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    nodebb_uid = models.IntegerField(unique=True)

    def __str__(self):
        return self.edx_uid.username
