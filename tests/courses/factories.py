from factory.django import DjangoModelFactory


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = "courses.Course"

    course_id = "bmHtyVrIEee3CwoIJ_9DVg"
    course_slug = "capstone-recommender-systems"
    course_name = "Capstone Recommender Systems"
