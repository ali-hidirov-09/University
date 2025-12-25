from rest_framework import serializers
from university.models import  *

class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class KafedraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kafedra
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


