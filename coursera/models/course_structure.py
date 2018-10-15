from django.db import models

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

    class Meta:
        managed = False
        db_table = "course_branch_items_view"
        unique_together = ("branch", "item_id")


class ItemType(models.Model):
    LECTURE = "lecture"

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
        managed = False
        db_table = "country2to3"
