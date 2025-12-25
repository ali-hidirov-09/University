from rest_framework import serializers
from university.models import Group, Grade, Teacher, Student
from django.contrib.auth import get_user_model
from university.services import  *

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = Grade
        fields = [
            "id",
            "student",
            "student_name",
            "subject",
            "subject_name",
            "rating",
            "semester",
            "created_at",
        ]
        read_only_fields = ("created_at",)


class TeacherSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Teacher
        fields = ("id", "user_id", "kafedra", 'username')


    def create(self, validated_data):
        request = self.context['request']
        target_user_id = validated_data.pop('user_id')
        kafedra = validated_data.pop('kafedra')

        User = get_user_model()
        target_user = User.objects.get(id=target_user_id)

        teacher = create_teacher(target_user, kafedra)
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Student
        fields = ('id','user_id', 'group', 'username')


    def create(self, validated_data):
        request = self.context['request']
        target_user_id = validated_data.pop('user_id')
        group = validated_data.pop('group')

        User = get_user_model()
        target_user = User.objects.get(id=target_user_id)

        student = create_student(target_user, group)
        return student

