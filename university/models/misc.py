from django.db import models
from django.contrib.auth.models import User


class University(models.Model):
    name = models.CharField(max_length=50, unique=True, )
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        unique_together = ('name', 'country')


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, max_length=100, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.university.name} - {self.name}'


class Kafedra(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.faculty.name} - {self.name}'


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE, null=True,blank=True)


    def __str__(self):
        return f"{self.user.username}"
