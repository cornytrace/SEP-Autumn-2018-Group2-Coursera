from django.db import models

__all__ = ["Assessment", "ItemAssessment"]


class Assessment(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column="assessment_id")
    base_id = models.CharField(max_length=50, db_column="assessment_base_id")
    version = models.IntegerField(db_column="assessment_version")
    type = models.CharField(max_length=50, db_column="assessment_type_desc")
    update_timestamp = models.DateTimeField(db_column="assessment_update_ts")
    passing_fraction = models.FloatField(db_column="assessment_passing_fraction")

    class Meta:
        managed = False
        db_table = "assessments_view"


class ItemAssessment(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_assessments",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        "Item",
        related_name="item_assessments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    assessment = models.ForeignKey(
        "Assessment",
        related_name="items",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_assessments_view"
        unique_together = ("item", "assessment")
