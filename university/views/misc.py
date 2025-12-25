from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from university.serializers import *
from university.models import University, Faculty, Kafedra
from rest_framework import viewsets, filters
from django_filters import rest_framework as dr
from university.permissions import IsStaffOrReadOnly
from university.filters import *


class CustomPagination(PageNumberPagination):
    page_size = 5


class UniversityViewsSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = CustomPagination

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    # filterset_class = UniversityFilter
    search_fields = ['name', 'country']



class FacultyViewsSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = CustomPagination

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = FacultyFilter
    search_fields = ['name', 'university__name']


class KafedraViewsSet(viewsets.ModelViewSet):
    queryset = Kafedra.objects.all()
    serializer_class = KafedraSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = CustomPagination

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = KafedraFilter
    search_fields = ['name', 'faculty__name', 'faculty__university__name', ]


class SubjectViewsSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = SubjectFilter
    search_fields = ['name', 'kafedra__name', 'kafedra__faculty__university__name', 'kafedra__faculty__name']


class GroupViewsSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsStaffOrReadOnly, IsAuthenticated]

    filter_backends = (dr.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = GroupFilter
    search_fields = ['name', 'faculty__name', 'faculty__university__name', 'subject__name', 'subject__kafedra__name', 'subject__kafedra__faculty__name', 'subject__kafedra__faculty__university__name']


