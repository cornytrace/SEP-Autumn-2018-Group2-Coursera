from django.db import models

__all__ = ["Course", "User", "CourseMembership"]


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=50)
    course_slug = models.CharField(max_length=2000, blank=True, null=True)
    course_name = models.CharField(max_length=2000, blank=True, null=True)
    course_launch_ts = models.DateTimeField(blank=True, null=True)
    course_update_ts = models.DateTimeField(blank=True, null=True)
    course_deleted = models.BooleanField(blank=True, null=True)
    course_graded = models.BooleanField(blank=True, null=True)
    course_desc = models.CharField(max_length=10000, blank=True, null=True)
    course_restricted = models.BooleanField(blank=True, null=True)
    course_verification_enabled_at_ts = models.DateTimeField(blank=True, null=True)
    primary_translation_equivalent_course_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    course_preenrollment_ts = models.DateTimeField(blank=True, null=True)
    course_workload = models.CharField(max_length=100, blank=True, null=True)
    course_session_enabled_ts = models.DateTimeField(blank=True, null=True)
    course_promo_photo_s3_bucket = models.CharField(
        max_length=255, blank=True, null=True
    )
    course_promo_photo_s3_key = models.CharField(
        max_length=10000, blank=True, null=True
    )
    course_level = models.CharField(max_length=50, blank=True, null=True)
    course_planned_launch_date_text = models.CharField(
        max_length=255, blank=True, null=True
    )
    course_header_image_s3_bucket = models.CharField(
        max_length=255, blank=True, null=True
    )
    course_header_image_s3_key = models.CharField(
        max_length=10000, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "courses"


class User(models.Model):
    eitdigital_user_id = models.CharField(primary_key=True, max_length=50)
    user_join_ts = models.DateTimeField(blank=True, null=True)
    country_cd = models.CharField(max_length=2, blank=True, null=True)
    region_cd = models.CharField(max_length=3, blank=True, null=True)
    profile_language_cd = models.CharField(max_length=8, blank=True, null=True)
    browser_language_cd = models.CharField(max_length=8, blank=True, null=True)
    reported_or_inferred_gender = models.CharField(max_length=50, blank=True, null=True)
    employment_status = models.CharField(max_length=100, blank=True, null=True)
    educational_attainment = models.CharField(max_length=100, blank=True, null=True)
    student_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"


class CourseMembership(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    eitdigital_user = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    course = models.ForeignKey(
        "Course", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    course_membership_role = models.CharField(max_length=50, blank=True, null=True)
    course_membership_ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "course_memberships_view"
