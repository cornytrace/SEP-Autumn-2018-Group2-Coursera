from django.db import models

__all__ = ["OnDemandSession"]


class OnDemandSession(models.Model):
    course_id = models.ForeignKey(
        "Course",
        related_name="sessions",
        on_delete=models.DO_NOTHING,
        db_column="course_id",
        max_length=50,
        blank=True,
        null=True,
    )
    id = models.CharField(
        db_column="on_demand_session_id", max_length=50, primary_key=True
    )
    start_timestamp = models.DateTimeField(
        db_column="on_demand_sessions_start_ts", blank=True, null=True
    )
    end_timestamp = models.DateTimeField(
        db_column="on_demand_sessions_end_ts", blank=True, null=True
    )
    enrollment_end_timestamp = models.DateTimeField(
        db_column="on_demand_sessions_enrollment_end_ts", blank=True, null=True
    )
    branch = models.ForeignKey(
        "Branch",
        related_name="sessions",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "on_demand_sessions"
