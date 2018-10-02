from django.db import models

__all__ = ["DiscussionQuestion"]


class DiscussionQuestion(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True, db_column="discussion_question_id"
    )
    eitdigital_discussions_user_id = models.CharField(max_length=50)
    discussion_question_title = models.CharField(
        max_length=20000, blank=True, null=True
    )
    discussion_question_details = models.CharField(
        max_length=20000, blank=True, null=True
    )
    discussion_question_context_type = models.CharField(
        max_length=50, blank=True, null=True
    )
    course_id = models.CharField(max_length=50, blank=True, null=True)
    course_module_id = models.CharField(max_length=50, blank=True, null=True)
    course_item_id = models.CharField(max_length=50, blank=True, null=True)
    discussion_forum_id = models.CharField(max_length=50, blank=True, null=True)
    country_cd = models.CharField(max_length=2, blank=True, null=True)
    group_id = models.CharField(max_length=50, blank=True, null=True)
    discussion_question_created_ts = models.DateTimeField(blank=True, null=True)
    discussion_question_updated_ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "discussion_questions"
