from django.urls import path, include
from rest_framework.routers import DefaultRouter
from university.views import *



router = DefaultRouter()
router.register(r"University", UniversityViewsSet)
router.register(r"Faculty", FacultyViewsSet)
router.register(r"Kafedra", KafedraViewsSet)
router.register(r"Subject", SubjectViewsSet)
router.register(r"Teacher", TeacherViewsSet)
router.register(r"Group", GroupViewsSet)
router.register(r"Student", StudentViewsSet)
router.register(r'Grade', GradeViewSet, basename='grade')

urlpatterns = [
    path('', include(router.urls)),
]