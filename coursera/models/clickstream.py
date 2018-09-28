from django.db import models

__all__ = ["ClickstreamEvent"]


class ClickstreamEvent(models.Model):
    id = models.CharField(max_length=100, primary_key=True, db_column="hashed_user_id")
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
    value = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "clickstream_events"
