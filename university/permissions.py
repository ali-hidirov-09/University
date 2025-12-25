from rest_framework import permissions
from university.models import Teacher

class IsStaffOrReadOnly(permissions.BasePermission):
    """ agar xodim staff member bo'lsa u edit va delete qila oladi """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsTeacherOrReadOnly(permissions.BasePermission):
    """ agar Teacher bo'lsa CRUD qila oladi, boshqalari faqat get qila oladi """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif Teacher.objects.filter(user=request.user).exists():
            return True
        return False

