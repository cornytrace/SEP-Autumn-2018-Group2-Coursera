from django.db import models

__all__ = ["EITDigitalUser", "CourseMembership"]


class EITDigitalUser(models.Model):
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

    memberships = models.ManyToManyField(
        "Course", through="CourseMembership", related_name="members"
    )

    class Meta:
        managed = False
        db_table = "users"


class CourseMembership(models.Model):
    PRE_ENROLLED_LEARNER = "PRE_ENROLLED_LEARNER"
    MENTOR = "MENTOR"
    TEACHING_STAFF = "TEACHING_STAFF"
    LEARNER = "LEARNER"
    INSTRUCTOR = "INSTRUCTOR"
    BROWSER = "BROWSER"
    NOT_ENROLLED = "NOT_ENROLLED"

    ROLE_CHOICES = (
        (PRE_ENROLLED_LEARNER, "Pre-enrolled learner"),
        (MENTOR, "Mentor"),
        (TEACHING_STAFF, "Teaching staff"),
        (LEARNER, "Learner"),
        (INSTRUCTOR, "Instructor"),
        (BROWSER, "Browser"),
        (NOT_ENROLLED, "Not enrolled"),
    )

    id = models.CharField(primary_key=True, max_length=50)
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="course_memberships", on_delete=models.DO_NOTHING
    )
    course = models.ForeignKey(
        "Course",
        related_name="course_memberships",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=ROLE_CHOICES,
        db_column="course_membership_role",
    )
    timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_membership_ts"
    )

    class Meta:
        managed = False
        db_table = "course_memberships_view"
        unique_together = ("eitdigital_user", "course", "timestamp")
