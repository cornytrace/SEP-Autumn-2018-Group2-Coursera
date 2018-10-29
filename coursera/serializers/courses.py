from datetime import timedelta
from functools import partial

from django.db.models import (
    Count,
    DateField,
    DateTimeField,
    F,
    OuterRef,
    Q,
    Subquery,
    Window,
)
from django.db.models.functions import Coalesce, TruncMonth
from django.utils.functional import cached_property
from django.utils.timezone import now
from rest_framework import serializers

from coursera.filters import GenericFilterSet
from coursera.models import (
    Branch,
    Course,
    CourseMembership,
    CourseProgress,
    CourseRating,
    EITDigitalUser,
    Grade,
    LastActivity,
    LastActivityPerModule,
    ModuleDuration,
)
from coursera.utils import AvgSubquery, CountSubquery

__all__ = ["CourseSerializer", "CourseAnalyticsSerializer"]


class CourseSerializer(serializers.ModelSerializer):
    """
    Serialize a Course with its basic properties and a few analytics.

    Calculates the following analytics:

    enrolled_learners: The number of learners enrolled in the course.
    leaving_learners: The number of enrolled learners that are no longer active.
    finished_learners: The number of learners that successfully completed the course.
    paying_learners: The number of learners that paid for the course.
    ratings: The ratings that students left at the end of the course.
    """

    class Meta:
        model = Course
        fields = [
            "id",
            "slug",
            "name",
            "specialization",
            "level",
            "enrolled_learners",
            "leaving_learners",
            "ratings",
            "finished_learners",
            "paying_learners",
        ]

    specialization = serializers.CharField()
    enrolled_learners = serializers.IntegerField()
    leaving_learners = serializers.SerializerMethodField()
    finished_learners = serializers.IntegerField()
    paying_learners = serializers.IntegerField()
    ratings = serializers.SerializerMethodField()

    @cached_property
    def filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    def _filter_current_branch(self, course_id):
        """
        Return a filtered queryset with just the current branch for `course_id`.
        """
        return Branch.objects.filter(
            pk=Subquery(
                Branch.objects.filter(course_id=course_id)
                .order_by(F("authoring_course_branch_created_ts").desc(nulls_last=True))
                .values("pk")[:1]
            )
        )

    def get_leaving_learners(self, obj):
        """
        Return the number of members for `obj` that have a LEARNER
        or PRE_ENROLLED_LEARNER status, have not finished the course
        and had their last activity more than 6 weeks before to_date,
        or today if the to_date filter isn't set. If from_date is set,
        calculate the difference in leaving learners between to_date and
        from_date.
        """
        form = GenericFilterSet(
            self.context["request"].GET,
            CourseMembership.objects.none(),
            request=self.context["request"],
        ).form
        form.errors
        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")

        if not to_date:
            to_date = now()

        if from_date and from_date > to_date:
            to_date = from_date

        if from_date:
            past_leavers = (
                CourseMembership.objects.filter(course_id=obj.pk)
                .filter(timestamp__lte=from_date)
                .filter(
                    role__in=[
                        CourseMembership.LEARNER,
                        CourseMembership.PRE_ENROLLED_LEARNER,
                    ]
                )
                .values("eitdigital_user_id")
                .difference(
                    Grade.objects.filter(course_id=obj.pk)
                    .filter(timestamp__lte=from_date)
                    .filter(passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED])
                    .values("eitdigital_user_id")
                )
                .difference(
                    LastActivity.objects.filter(course_id=obj.pk)
                    .filter(timestamp__gt=from_date - timedelta(weeks=6))
                    .values("eitdigital_user_id")
                )
                .count()
            )
        else:
            past_leavers = 0

        return (
            CourseMembership.objects.filter(course_id=obj.pk)
            .filter(timestamp__lte=to_date)
            .filter(
                role__in=[
                    CourseMembership.LEARNER,
                    CourseMembership.PRE_ENROLLED_LEARNER,
                ]
            )
            .values("eitdigital_user_id")
            .difference(
                Grade.objects.filter(course_id=obj.pk)
                .filter(timestamp__lte=to_date)
                .filter(passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED])
                .values("eitdigital_user_id")
            )
            .difference(
                LastActivity.objects.filter(course_id=obj.pk)
                .filter(timestamp__gt=to_date - timedelta(weeks=6))
                .values("eitdigital_user_id")
            )
            .count()
            - past_leavers
        )

    def get_ratings(self, obj):
        """
        Return the number of ratings for each rating from 1 to 10 for `obj`,
        from either a first-week or end-of-course Net Promotor Score (NPS).
        """
        try:
            ratings = obj.ratings
        except AttributeError:
            ratings = list(
                self.filter(CourseRating.objects.filter(course_id=obj.pk))
                .filter(
                    feedback_system__in=[
                        CourseRating.NPS_FIRST_WEEK,
                        CourseRating.NPS_END_OF_COURSE,
                    ]
                )
                .values_list("rating")
                .annotate(Count("id"))
                .order_by("rating")
            )
        missing = set(range(1, 11)) - {rating for rating, _ in ratings}
        for i in missing:
            ratings.insert(i - 1, (i, 0))
        return ratings


class CourseAnalyticsSerializer(CourseSerializer):
    """
    Serialize a Course with its basic properties and
    additional analytics.

    Calculates the following analytics:

    modules: The number of modules in the course.
    quizzes: The number of quizzes in the course.
    assignments: The number of assignments in the course.
    videos: The number of videos in the course.
    cohorts: The number of cohorts in the course.
    finished_learners_over_time: The cumulative number of students that finished the course per month.
    leaving_learners_per_module: The number of students per module that had their last activity in that module.
    average_time: The average time between a student's first and last activity in the course.
    average_time_per_module: The average time between a student's first and last activity in a module.
    geo_data: The number of enrolled students per country.
    cohort_list: The start and end dates of a cohort.
    """

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + [
            "modules",
            "quizzes",
            "assignments",
            "videos",
            "cohorts",
            "finished_learners_over_time",
            "leaving_learners_per_module",
            "average_time",
            "average_time_per_module",
            "geo_data",
            "cohort_list",
        ]

    modules = serializers.IntegerField()
    quizzes = serializers.IntegerField()
    assignments = serializers.IntegerField()
    videos = serializers.IntegerField()
    cohorts = serializers.IntegerField()
    finished_learners_over_time = serializers.SerializerMethodField()
    leaving_learners_per_module = serializers.SerializerMethodField()
    average_time = serializers.SerializerMethodField()
    average_time_per_module = serializers.SerializerMethodField()
    geo_data = serializers.SerializerMethodField()
    cohort_list = serializers.SerializerMethodField()

    def get_finished_learners_over_time(self, obj):
        """
        For each month, show the cumulative number of students that has passed
        the course `obj`.
        """
        try:
            return obj.finished_learners_over_time
        except AttributeError:
            return list(
                Grade.objects.filter(course_id=obj.pk)
                .annotate(month=TruncMonth("timestamp", output_field=DateField()))
                .annotate(
                    num_finished=Window(
                        Count(
                            "course_id",
                            filter=Q(
                                passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED]
                            ),
                        ),
                        order_by=TruncMonth("timestamp").asc(),
                    )
                )
                .order_by(TruncMonth("timestamp").asc())
                .values_list("month", "num_finished")
                .distinct()
            )

    def get_leaving_learners_per_module(self, obj):
        """
        For each module in course `obj`, get the number of learners who
        haven't passed the course and whose activity furtherst in the course
        was in that module.
        """
        form = GenericFilterSet(
            self.context["request"].GET,
            CourseMembership.objects.none(),
            request=self.context["request"],
        ).form
        form.errors
        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")

        if not to_date:
            to_date = now()

        if from_date and from_date > to_date:
            to_date = from_date

        subquery = CountSubquery(
            LastActivityPerModule.objects.filter(module_id=OuterRef("pk")).filter(
                timestamp__lt=to_date - timedelta(weeks=6)
            )
        )
        if from_date:
            subquery -= CountSubquery(
                LastActivityPerModule.objects.filter(module_id=OuterRef("pk")).filter(
                    timestamp__lt=from_date - timedelta(weeks=6)
                )
            )

        return list(
            self._filter_current_branch(obj.pk)
            .get()
            .modules.values_list("module_id")
            .annotate(user_count=subquery)
            .order_by("order")
        )

    def get_average_time(self, obj):
        return obj.average_time

    def get_average_time_per_module(self, obj):
        """
        For each module in course `obj`, return the average duration between
        each learners first activity and last activity in that module.
        """
        return list(
            self._filter_current_branch(obj.pk)
            .get()
            .modules.values_list("module_id")
            .annotate(
                average_time=Coalesce(
                    AvgSubquery(
                        self.filter(
                            ModuleDuration.objects.filter(
                                module_id=OuterRef("pk")
                            ).values("duration")
                        ),
                        db_column="duration",
                        output_field=DateTimeField(),
                    ),
                    timedelta(0),
                )
            )
            .order_by("order")
        )

    def get_geo_data(self, obj):
        """
        Return the count of countries of users of the course.
        """
        try:
            return obj.geo_data
        except AttributeError:
            return list(
                EITDigitalUser.objects.filter(
                    eitdigital_user_id__in=CourseMembership.objects.filter(
                        course_id=obj.pk
                    )
                    .filter(
                        role__in=[
                            CourseMembership.LEARNER,
                            CourseMembership.PRE_ENROLLED_LEARNER,
                        ]
                    )
                    .values("eitdigital_user_id")
                )
                .annotate(three_let=F("country_cd__three_let"))
                .annotate(country_name=F("country_cd__country"))
                .values_list("three_let", "country_name")
                .annotate(country_count=Count("eitdigital_user_id"))
            )

    def get_cohort_list(self, obj):
        return list(
            obj.sessions.values_list("timestamp", "end_timestamp").order_by("timestamp")
        )
