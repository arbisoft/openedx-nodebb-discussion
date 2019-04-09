"""
Models to save required data to sync edx with nodebb.
"""
from django.contrib.auth.models import User
from django.db import models

from opaque_keys.edx.django.models import CourseKeyField


class EdxNodeBBUser(models.Model):
    edx_uid = models.OneToOneField(User, on_delete=models.CASCADE)
    nodebb_uid = models.IntegerField(unique=True)

    def __str__(self):
        return self.edx_uid.username


class EdxNodeBBCategory(models.Model):
    course_key = CourseKeyField(max_length=255, db_index=True)
    nodebb_cid = models.IntegerField(unique=True)
    nodebb_group_slug = models.CharField(max_length=255, blank=True, null=True)
    nodebb_group_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.course_key)
