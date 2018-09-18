import factory
from django.utils.crypto import get_random_string
from factory.django import DjangoModelFactory


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = "courses.Course"

    course_id = factory.LazyFunction(get_random_string)
    course_slug = "capstone-recommender-systems"
    course_name = "Capstone Recommender Systems"
