from django.db.models import FloatField, Func, IntegerField, Subquery


class NullIf(Func):
    function = "NULLIF"


class CountSubquery(Subquery):
    template = "(SELECT COUNT(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()


class AvgSubquery(Subquery):
    template = "(SELECT AVG(%(field)s) FROM (%(subquery)s) _avg)"
    output_field = FloatField()
