from django.contrib.postgres.fields import JSONField
from django.db import models

__all__ = ["ClickstreamEvent", "Heartbeat"]


class ClickstreamEvent(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    eitdigital_user_id = models.CharField(max_length=100, db_column="hashed_user_id")
    hashed_session_cookie_id = models.CharField(max_length=100, blank=True, null=True)
    server_timestamp = models.DateTimeField(blank=True, null=True)
    hashed_ip = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    initial_referrer_url = models.CharField(max_length=100, blank=True, null=True)
    browser_language = models.CharField(max_length=100, blank=True, null=True)
    course_id = models.CharField(max_length=100, blank=True, null=True)
    country_cd = models.CharField(max_length=100, blank=True, null=True)
    region_cd = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    key = models.CharField(max_length=100, blank=True, null=True)
    value = JSONField()

    class Meta:
        managed = False
        db_table = "clickstream_events_view"


class Heartbeat(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    course = models.ForeignKey(
        "Course", on_delete=models.DO_NOTHING, related_name="heartbeats"
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", on_delete=models.DO_NOTHING, related_name="heartbeats"
    )
    module = models.ForeignKey(
        "Module", on_delete=models.DO_NOTHING, related_name="heartbeats"
    )
    item = models.ForeignKey(
        "Item", on_delete=models.DO_NOTHING, related_name="heartbeats"
    )
    timecode = models.IntegerField()
    server_timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "heartbeat_events_view"
