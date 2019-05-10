"""
Models to save required data to sync edx with nodebb.
"""
from django.contrib.auth.models import User
from django.db import models
from opaque_keys.edx.django.models import CourseKeyField


class EdxNodeBBUser(models.Model):
    """
    Stores NodeBB uid against edX User
    """
    edx_uid = models.OneToOneField(User, on_delete=models.CASCADE)
    nodebb_uid = models.IntegerField(unique=True)

    def __str__(self):
        return self.edx_uid.username


class EdxNodeBBCategory(models.Model):
    """
    Stores NodeBB cid, group_slug and group_name against edX Courses
    """
    course_key = CourseKeyField(max_length=255, db_index=True)
    nodebb_cid = models.IntegerField(primary_key=True)
    nodebb_group_slug = models.SlugField(max_length=255, blank=True, null=True)
    nodebb_group_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.course_key)


class EdxNodeBBEnrollment(models.Model):
    """
    Stores Edx Course Id and Edx User Id to keep record of Edx Enrollments.
    """
    course_key = CourseKeyField(max_length=255, db_index=True)
    edx_uid = models.ForeignKey(User, on_delete=models.CASCADE)
    nodebb_cid = models.ForeignKey(EdxNodeBBCategory, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.edx_uid.username, str(self.course_key))
