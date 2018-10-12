from datetime import timedelta

from django.db import models
from django.db.models import Avg, Count, F, Max, Min, OuterRef, Q, Subquery, Window
from django.db.models.functions import Coalesce, TruncMonth
from django.utils.timezone import now

from coursera.utils import AvgSubquery, CountSubquery

from .activities import CourseProgress
from .assessments import ItemAssessment
from .course_structure import Item, ItemType, Module
from .feedback import CourseRating
from .grades import Grade
from .sessions import OnDemandSession
from .users import CourseMembership

__all__ = ["Course", "Branch", "ItemProgrammingAssignment", "ItemPeerAssignment"]


class CourseQuerySet(models.QuerySet):
    def filter_current_branch(self):
        return self.filter(
            branches=Subquery(
                Branch.objects.filter(course_id=OuterRef("id"))
                .order_by(F("authoring_course_branch_created_ts").desc(nulls_last=True))
                .values("pk")[:1]
            )
        )

    def with_enrolled_learners(self, filter):
        return self.annotate(
            enrolled_learners=CountSubquery(
                filter(
                    CourseMembership.objects.filter(course_id=OuterRef("pk")).filter(
                        role__in=[
                            CourseMembership.LEARNER,
                            CourseMembership.PRE_ENROLLED_LEARNER,
                        ]
                    )
                )
            )
        )

    def with_leaving_learners(self):  # pragma: no cover
        return self.annotate(
            leaving_learners=CountSubquery(
                CourseMembership.objects.filter(course_id=OuterRef("pk"))
                .filter(
                    role__in=[
                        CourseMembership.LEARNER,
                        CourseMembership.PRE_ENROLLED_LEARNER,
                    ]
                )
                .values("eitdigital_user_id")
                .difference(
                    Grade.objects.filter(course_id=OuterRef("pk"))
                    .filter(passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED])
                    .values("eitdigital_user_id")
                )
                .difference(
                    CourseProgress.objects.filter(course_id=OuterRef("pk"))
                    .filter(timestamp__gt=now() - timedelta(weeks=6))
                    .values("eitdigital_user_id")
                )
            )
        )

    def with_finished_learners(self, filter):
        return self.annotate(
            finished_learners=CountSubquery(
                filter(
                    Grade.objects.filter(course_id=OuterRef("pk")).filter(
                        passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED]
                    )
                )
            )
        )

    def with_modules(self):
        return self.annotate(
            modules=CountSubquery(
                Module.objects.filter(branch_id=OuterRef("branches__pk"))
            )
        )

    def with_quizzes(self):
        return self.annotate(
            quizzes=CountSubquery(
                ItemAssessment.objects.filter(branch_id=OuterRef("branches__pk"))
            )
        )

    def with_assignments(self):
        return self.annotate(
            assignments=CountSubquery(
                ItemProgrammingAssignment.objects.filter(
                    branch_id=OuterRef("branches__pk")
                )
            )
            + CountSubquery(
                ItemPeerAssignment.objects.filter(branch_id=OuterRef("branches__pk"))
            )
        )

    def with_videos(self):
        return self.annotate(
            videos=CountSubquery(
                Item.objects.filter(branch_id=OuterRef("branches__pk")).filter(
                    type__description=ItemType.LECTURE
                )
            )
        )

    def with_cohorts(self, filter):
        return self.annotate(
            cohorts=CountSubquery(
                filter(OnDemandSession.objects.filter(course_id=OuterRef("pk")))
            )
        )

    def with_average_time(self, filter):
        return self.annotate(
            average_time=Coalesce(
                AvgSubquery(
                    CourseProgress.objects.filter(course_id=OuterRef("pk"))
                    .values("eitdigital_user_id")
                    .annotate(time_spent=Max("timestamp") - Min("timestamp"))
                    .values("time_spent"),
                    db_column="time_spent",
                    output_field=models.DurationField(),
                ),
                timedelta(0),
            )
        )


class Course(models.Model):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

    COURSE_LEVELS = (
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    id = models.CharField(primary_key=True, max_length=50, db_column="course_id")
    slug = models.CharField(
        max_length=2000, blank=True, null=True, db_column="course_slug"
    )
    name = models.CharField(
        max_length=2000, blank=True, null=True, db_column="course_name"
    )
    launch_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_launch_ts"
    )
    update_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_update_ts"
    )
    deleted = models.BooleanField(blank=True, null=True, db_column="course_deleted")
    graded = models.BooleanField(blank=True, null=True, db_column="course_graded")
    description = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_desc"
    )
    restricted = models.BooleanField(
        blank=True, null=True, db_column="course_restricted"
    )
    verification_enabled_at_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_verification_enabled_at_ts"
    )
    primary_translation_equivalent_course_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    preenrollment_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_preenrollment_ts"
    )
    workload = models.CharField(
        max_length=100, blank=True, null=True, db_column="course_workload"
    )
    session_enabled_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_session_enabled_ts"
    )
    promo_photo_s3_bucket = models.CharField(
        max_length=255, blank=True, null=True, db_column="course_promo_photo_s3_bucket"
    )
    promo_photo_s3_key = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_promo_photo_s3_key"
    )
    level = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=COURSE_LEVELS,
        db_column="course_level",
    )
    planned_launch_date_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="course_planned_launch_date_text",
    )
    header_image_s3_bucket = models.CharField(
        max_length=255, blank=True, null=True, db_column="course_header_image_s3_bucket"
    )
    header_image_s3_key = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_header_image_s3_key"
    )

    objects = CourseQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = "courses"


class Branch(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column="course_branch_id")
    course = models.ForeignKey(
        "Course",
        related_name="branches",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    changes_description = models.CharField(
        max_length=65535,
        blank=True,
        null=True,
        db_column="course_branch_changes_description",
    )
    authoring_course_branch_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    authoring_course_branch_created_ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "course_branches"


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
        max_length=50,
        blank=True,
        null=True,
    )
    course_item_id = models.ForeignKey(
        "Item",
        related_name="item_peer_assignments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    peer_assignment_id = models.CharField(
        db_column="peer_assignment_id", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_peer_assignments_view"
