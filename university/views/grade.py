from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from university.serializers import *
from university.models import Grade, Teacher, Student
from rest_framework import viewsets, filters
from django_filters import rest_framework as dr
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from university.filters import *
from university.permissions import IsStaffOrReadOnly, IsTeacherOrReadOnly


class CustomPagination(PageNumberPagination):
    page_size = 5


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsTeacherOrReadOnly]

    filter_backends = (dr.DjangoFilterBackend,)
    filterset_class = GradeFilter

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Grade.objects.all()

        if hasattr(user, "student"):
            return Grade.objects.filter(student=user.student)

        if hasattr(user, "teacher"):
            return Grade.objects.filter(
                subject__kafedra=user.teacher.kafedra
            )

        return Grade.objects.none()


class TeacherViewsSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TeacherFilter
    search_fields = ['user__username', 'kafedra__name', 'kafedra__faculty__name', 'kafedra__faculty__university__name']


class StudentViewsSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = StudentFilter
    search_fields = [
        'user__username',
        'group__name',
        'group__faculty__name',
        'group__faculty__university__name',
        'group__subject__name',
        'group__subject__kafedra__name',
        'group__subject__kafedra__faculty__name',
        'group__subject__kafedra__faculty__university__name',
    ]
