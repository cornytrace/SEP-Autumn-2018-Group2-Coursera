from django.contrib import admin

from courses.models import Course


class CourseAdmin(admin.ModelAdmin):
    fields = ["course_id", "course_slug", "course_name"]
    list_display = ["course_id", "course_slug", "course_name"]


admin.site.register(Course, CourseAdmin)
