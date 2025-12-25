from django.db import models
from django.contrib.auth.models import User
from .misc import Kafedra, Faculty
from django.core.validators import MaxValueValidator, MinValueValidator


class Subject(models.Model):
    name = models.CharField(max_length=100)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.kafedra.name} - {self.name}'


class Group(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.faculty} - {self.name}'

    class Meta:
        unique_together = ('name', 'faculty')



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"



class Grade(models.Model):
    SEMESTER_CHOICES = [
        (1, '1-semester'),
        (2, '2-semester'),
        (3, '3-semester'),
        (4, '4-semester'),
        (5, '5-semester'),
        (6, '6-semester'),
        (7, '7-semester'),
        (8, '8-semester'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester')


    def __str__(self):
        return f'{self.student} - {self.subject} - {self.rating} ({self.semester}-semester)'


    def add_rating(self, ratingg):
        if ratingg > 10 or ratingg < 0:
            raise ValueError("Invalid rating")
        self.rating = ratingg
        self.save()



