from django.db import models

__all__ = [
    "PeerAssignment",
    "PeerSubmission",
    "ItemProgrammingAssignment",
    "ItemPeerAssignment",
]


class PeerAssignment(models.Model):
    id = models.CharField(
        db_column="peer_assignment_id", max_length=50, primary_key=True
    )
    base_id = models.CharField(
        db_column="peer_assignment_base_id", max_length=50, blank=True, null=True
    )
    type = models.CharField(
        db_column="peer_assignment_type", max_length=50, blank=True, null=True
    )
    required_review_count = models.IntegerField(
        db_column="peer_assignment_required_review_count", blank=True, null=True
    )
    passing_fraction = models.FloatField(
        db_column="peer_assignment_passing_fraction", blank=True, null=True
    )
    required_reviewer_count_for_score = models.IntegerField(
        db_column="peer_assignment_required_reviewer_count_for_score",
        blank=True,
        null=True,
    )
    required_wait_for_score_ms = models.BigIntegerField(
        db_column="peer_assignment_required_wait_for_score_ms", blank=True, null=True
    )
    maximum_score = models.FloatField(
        db_column="peer_assignment_maximum_score", blank=True, null=True
    )
    update_ts = models.DateTimeField(
        db_column="peer_assignment_update_ts", blank=True, null=True
    )
    is_mentor_graded = models.BooleanField(
        db_column="peer_assignment_is_mentor_graded", blank=True, null=True
    )

    items = models.ManyToManyField(
        "Item", through="ItemPeerAssignment", related_name="peer_assignments"
    )

    class Meta:
        managed = False
        db_table = "peer_assignments_view"


class PeerSubmission(models.Model):
    id = models.CharField(
        db_column="peer_submission_id", max_length=50, primary_key=True
    )
    peer_assignment = models.ForeignKey(
        "PeerAssignment",
        related_name="submissions",
        on_delete=models.DO_NOTHING,
        db_column="peer_assignment_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="peer_submissions",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
    )
    timestamp = models.DateTimeField(db_column="peer_submission_created_ts")
    is_draft = models.BooleanField(
        db_column="peer_submission_is_draft", blank=True, null=True
    )
    title = models.CharField(
        db_column="peer_submission_title", max_length=65535, blank=True, null=True
    )
    removed_from_public_ts = models.DateTimeField(
        db_column="peer_submission_removed_from_public_ts", blank=True, null=True
    )
    score_available_ts = models.DateTimeField(
        db_column="peer_submission_score_available_ts", blank=True, null=True
    )
    score = models.FloatField(db_column="peer_submission_score", blank=True, null=True)
    is_mentor_graded = models.BooleanField(
        db_column="peer_submission_is_mentor_graded", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "peer_submissions_view"


class ItemProgrammingAssignment(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_programming_assignments",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )
    course_item_id = models.ForeignKey(
        "Item",
        related_name="item_programming_assignments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    programming_assignment_id = models.CharField(
        db_column="programming_assignment_id", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_programming_assignments_view"


class ItemPeerAssignment(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_peer_assignments",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
    )
    item = models.ForeignKey(
        "Item",
        related_name="item_peer_assignments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
    )
    peer_assignment = models.ForeignKey(
        "PeerAssignment",
        related_name="item_peer_assignments",
        on_delete=models.DO_NOTHING,
        db_column="peer_assignment_id",
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_peer_assignments_view"
