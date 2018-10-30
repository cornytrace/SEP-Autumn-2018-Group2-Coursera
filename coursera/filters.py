import django_filters

from coursera.models import ClickstreamEvent


class ClickstreamEventFilterSet(django_filters.FilterSet):
    """
    FilterSet to filter clickstream events with a server_timestamp within
    the given timespan.
    """

    from_date = django_filters.DateTimeFilter(
        field_name="server_timestamp", lookup_expr="gte"
    )
    to_date = django_filters.DateTimeFilter(
        field_name="server_timestamp", lookup_expr="lte"
    )

    class Meta:
        model = ClickstreamEvent
        fields = ["from_date", "to_date"]


class GenericFilterSet(django_filters.FilterSet):
    """
    Generic FilterSet to filter any model with a "timestamp" field within the
    given timespan.
    """

    from_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    to_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
