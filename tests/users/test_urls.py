from django.urls import reverse


def test_admin_urls_are_configured():
    assert reverse("admin:index") == "/admin/", "admin urls are not configured"
