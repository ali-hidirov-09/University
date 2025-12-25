from django_filters import rest_framework as django_filters
from .models import *



class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = ("group",)


class UniversityFilter(django_filters.FilterSet):
    class Meta:
        model = University
        fields = ("country",)


class FacultyFilter(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = ("university",)


class KafedraFilter(django_filters.FilterSet):
    class Meta:
        model = Kafedra
        fields = ("faculty",'faculty__university__id')


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ("faculty",'subject')


class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = ("kafedra",'kafedra__faculty__id', 'kafedra__faculty__university__id')


class TeacherFilter(django_filters.FilterSet):
    class Meta:
        model = Teacher
        fields = ("kafedra",'kafedra__faculty__id', 'kafedra__faculty__university__id')



class GradeFilter(django_filters.FilterSet):
    semester = django_filters.NumberFilter()
    subject = django_filters.NumberFilter()
    student = django_filters.NumberFilter()
    group = django_filters.NumberFilter(field_name="student__group")
    faculty = django_filters.NumberFilter(field_name="student__group__faculty")
    kafedra = django_filters.NumberFilter(field_name="subject__kafedra")

    class Meta:
        model = Grade
        fields = (
            "semester",
            "subject",
            "student",
            "group",
            "faculty",
            "kafedra",
        )