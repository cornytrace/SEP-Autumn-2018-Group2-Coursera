from django.db import models

__all__ = ["Specialization", "CourseSpecialization"]


class Specialization(models.Model):
    id = models.CharField(db_column="specialization_id", primary_key=True)
    slug = models.CharField(db_column="specialization_slug", max_length=255)
    name = models.CharField(db_column="specialization_name", max_length=2000)
    display_page_launch_ts = models.DateTimeField(
        db_column="specialization_display_page_launch_ts"
    )
    sequence_branch_id = models.CharField(
        db_column="sequence_branch_id", max_length=255
    )
    version = models.BigIntegerField(db_column="specialization_version")
    base_id = models.CharField(db_column="base_specialization_id", max_length=255)
    primary_domain = models.CharField(
        db_column="specialization_primary_domain", max_length=255
    )
    primary_subdomain = models.CharField(
        db_column="specialization_primary_subdomain", max_length=255
    )

    courses = models.ManyToManyField(
        "Course", through="CourseSpecialization", related_name="specializations"
    )

    class Meta:
        managed = False
        db_table = "specializations_view"


class CourseSpecialization(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    course = models.ForeignKey(
        "Course", related_name="course_specializations", on_delete=models.DO_NOTHING
    )
    specialization = models.ForeignKey(
        "Specialization",
        related_name="course_specializations",
        on_delete=models.DO_NOTHING,
    )
    current_dt = models.DateField(db_column="current_dt")

    class Meta:
        managed = False
        db_table = "specializations_courses_view"
        unique_together = ("course", "specialization")
