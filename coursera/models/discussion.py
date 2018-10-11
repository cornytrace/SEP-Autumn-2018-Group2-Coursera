from django.db import models

__all__ = ["DiscussionQuestion"]


class DiscussionQuestion(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True, db_column="discussion_question_id"
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="discussion_questions",
        on_delete=models.DO_NOTHING,
    )
    discussion_question_title = models.CharField(
        max_length=20000, blank=True, null=True
    )
    discussion_question_details = models.CharField(
        max_length=20000, blank=True, null=True
    )
    discussion_question_context_type = models.CharField(
        max_length=50, blank=True, null=True
    )
    course = models.ForeignKey(
        "Course", related_name="discussion_questions", on_delete=models.DO_NOTHING
    )
    module = models.ForeignKey(
        "Module",
        related_name="discussion_questions",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    item = models.ForeignKey(
        "Item",
        related_name="discussion_questions",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    discussion_forum_id = models.CharField(max_length=50, blank=True, null=True)
    country_cd = models.CharField(max_length=2, blank=True, null=True)
    group_id = models.CharField(max_length=50, blank=True, null=True)
    discussion_question_created_ts = models.DateTimeField(blank=True, null=True)
    discussion_question_updated_ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "discussion_questions_view"
