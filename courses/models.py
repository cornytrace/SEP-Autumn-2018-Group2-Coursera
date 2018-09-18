from django.db import models


class Course(models.Model):
    course_id = models.CharField(unique=True, max_length=30)
    course_slug = models.CharField(unique=True, max_length=100)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course_name}"
