from django.contrib.auth.models import User
from django.db import models
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField


class NodeBBUserRelation(models.Model):
    edx_uid = models.OneToOneField(User, on_delete=models.CASCADE)
    nodebb_uid = models.IntegerField(unique=True)

    def __str__(self):
        return self.edx_uid.username


class NodeBBCategoryRelation(models.Model):
    course_key = CourseKeyField(max_length=255, db_index=True)
    nodebb_cid = models.IntegerField(unique=True)
    nodebb_group_slug = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.course_key)
