from django.db import models
from django.db.models import OuterRef
from django.db.models.functions import Cast, Coalesce

from coursera.utils import AvgSubquery, CountSubquery, NullIf

from .activities import CourseProgress
from .assignments import PeerAssignment, PeerSubmission
from .grades import ItemGrade

__all__ = ["Module", "Lesson", "Item", "ItemType", "Country2To3"]


class Module(models.Model):
    id = models.CharField(primary_key=True, max_length=50, db_column="module_id")
    branch = models.ForeignKey(
        "Branch",
        related_name="modules",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_column="course_branch_id",
    )
    module_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="course_module_id"
    )
    order = models.IntegerField(
        blank=True, null=True, db_column="course_branch_module_order"
    )
    name = models.CharField(
        max_length=2000, blank=True, null=True, db_column="course_branch_module_name"
    )
    description = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_branch_module_desc"
    )

    class Meta:
        managed = False
        db_table = "course_branch_modules_view"
        unique_together = ("branch", "module_id")


class Lesson(models.Model):
    id = models.CharField(primary_key=True, max_length=50, db_column="lesson_id")
    branch = models.ForeignKey(
        "Branch",
        related_name="lessons",
        on_delete=models.DO_NOTHING,
        max_length=50,
        blank=True,
        null=True,
        db_column="course_branch_id",
    )
    lesson_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="course_lesson_id"
    )
    module = models.ForeignKey(
        "Module",
        related_name="lessons",
        on_delete=models.DO_NOTHING,
        db_column="module_id",
    )
    order = models.IntegerField(
        blank=True, null=True, db_column="course_branch_lesson_order"
    )
    name = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_branch_lesson_name"
    )

    class Meta:
        managed = False
        db_table = "course_branch_lessons_view"
        unique_together = ("branch", "lesson_id")


class PeerAssignmentQuerySet(models.QuerySet):
    def with_submissions(self, filter):
        return self.annotate(
            submissions=CountSubquery(
                filter(
                    PeerSubmission.objects.filter(peer_assignment__items=OuterRef("pk"))
                )
            )
        )

    def with_submission_ratio(self, filter):
        return self.annotate(
            submission_ratio=Coalesce(
                Cast(
                    CountSubquery(
                        filter(
                            PeerSubmission.objects.filter(
                                peer_assignment__items=OuterRef("pk")
                            )
                            .values_list("eitdigital_user_id")
                            .distinct()
                        )
                    ),
                    models.FloatField(),
                )
                / NullIf(
                    CountSubquery(
                        filter(
                            CourseProgress.objects.filter(item_id=OuterRef("pk"))
                            .values_list("eitdigital_user_id")
                            .distinct()
                        )
                    ),
                    0,
                    output_field=models.FloatField(),
                ),
                0,
            )
        )

    def with_average_grade(self, filter):
        subquery = filter(
            ItemGrade.objects.filter(item=OuterRef("pk"))
            .annotate(
                grade=Cast(
                    "overall", models.DecimalField(max_digits=3, decimal_places=2)
                )
            )
            .values_list("grade")
        )
        return self.annotate(
            average_grade=Coalesce(AvgSubquery(subquery, db_column="grade"), 0)
        )


class PeerAssignmentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                type__description__in=[
                    ItemType.PEER,
                    ItemType.PHASED_PEER,
                    ItemType.GRADED_PEER,
                    ItemType.CLOSED_PEER,
                ]
            )
        )


class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=50, db_column="item_id")
    branch = models.ForeignKey(
        "Branch",
        related_name="items",
        on_delete=models.DO_NOTHING,
        max_length=255,
        blank=True,
        null=True,
        db_column="course_branch_id",
    )
    item_id = models.CharField(
        max_length=255, blank=True, null=True, db_column="course_item_id"
    )
    lesson = models.ForeignKey(
        "Lesson",
        related_name="items",
        on_delete=models.DO_NOTHING,
        max_length=255,
        blank=True,
        null=True,
        db_column="lesson_id",
    )
    order = models.IntegerField(
        blank=True, null=True, db_column="course_branch_item_order"
    )
    type = models.ForeignKey(
        "ItemType",
        related_name="+",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_column="course_item_type_id",
    )
    name = models.CharField(
        max_length=255, blank=True, null=True, db_column="course_branch_item_name"
    )
    optional = models.NullBooleanField(
        blank=True, db_column="course_branch_item_optional"
    )
    atom_id = models.CharField(max_length=255, blank=True, null=True)
    atom_version_id = models.IntegerField(blank=True, null=True)
    atom_is_frozen = models.NullBooleanField(
        blank=True, db_column="course_branch_atom_is_frozen"
    )

    objects = models.Manager()
    peer_assignment_objects = PeerAssignmentManager.from_queryset(
        PeerAssignmentQuerySet
    )()

    class Meta:
        managed = False
        db_table = "course_branch_items_view"
        unique_together = ("branch", "item_id")


class ItemType(models.Model):
    LECTURE = "lecture"
    PEER = "peer"
    PHASED_PEER = "phased peer"
    GRADED_PEER = "graded peer"
    CLOSED_PEER = "closed peer"

    id = models.IntegerField(db_column="course_item_type_id", primary_key=True)
    description = models.CharField(
        db_column="course_item_type_desc", max_length=255, blank=True, null=True
    )
    category = models.CharField(
        db_column="course_item_type_category", max_length=255, blank=True, null=True
    )
    graded = models.BooleanField(
        db_column="course_item_type_graded", blank=True, null=True
    )
    atom_content_type_id = models.IntegerField(
        db_column="atom_content_type_id", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "course_item_types"


class Country2To3(models.Model):
    country = models.CharField(max_length=100)
    two_let = models.CharField(max_length=2, primary_key=True)
    three_let = models.CharField(max_length=3)

    class Meta:
        db_table = "country2to3"
