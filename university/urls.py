from django.urls import path, include
from rest_framework.routers import DefaultRouter
from university.views import UniversityViewsSet, GradeViewSet, FacultyViewsSet, KafedraViewsSet, SubjectViewsSet, \
    TeacherViewsSet, GroupViewsSet, StudentViewsSet


router = DefaultRouter()
router.register(r"university", UniversityViewsSet)
router.register(r"faculty", FacultyViewsSet)
router.register(r"kafedra", KafedraViewsSet)
router.register(r"subject", SubjectViewsSet)
router.register(r"teacher", TeacherViewsSet)
router.register(r"group", GroupViewsSet)
router.register(r"student", StudentViewsSet)
router.register(r'grade', GradeViewSet, basename='grade')

urlpatterns = [
    path('', include(router.urls)),
]