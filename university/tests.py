from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from university.models import (
    University, Faculty, Kafedra, Subject,
    Group, Student, Teacher, Grade
)
from university.services.misc import create_teacher, create_student

# university
# faculty
# kafedra
# subject
# teacher
# group
# student
# grade

def make_base_data():
    """Test uchun kerakli barcha asosiy obyektlarni yaratadi."""
    university = University.objects.create(name="TUIT", country="Uzbekistan")
    faculty = Faculty.objects.create(name="CS Faculty", university=university)
    kafedra = Kafedra.objects.create(name="Backend Dept", faculty=faculty)
    subject = Subject.objects.create(name="Python", kafedra=kafedra)
    group = Group.objects.create(name="CS-101", faculty=faculty, subject=subject)
    return university, faculty, kafedra, subject, group



class UniversityModelTest(TestCase):

    def test_university_created(self):
        uni = University.objects.create(name="TUIT", country="Uzbekistan")
        self.assertEqual(uni.name, "TUIT")
        self.assertEqual(str(uni), "TUIT")

    def test_university_unique_name(self):
        University.objects.create(name="TUIT", country="Uzbekistan")
        with self.assertRaises(Exception):
            University.objects.create(name="TUIT", country="Uzbekistan")


class FacultyModelTest(TestCase):

    def setUp(self):
        self.uni = University.objects.create(name="TUIT", country="Uzbekistan")

    def test_faculty_str(self):
        faculty = Faculty.objects.create(name="CS", university=self.uni)
        self.assertEqual(str(faculty), "TUIT - CS")


class KafedraModelTest(TestCase):

    def setUp(self):
        uni = University.objects.create(name="TUIT", country="Uzbekistan")
        self.faculty = Faculty.objects.create(name="CS", university=uni)

    def test_kafedra_str(self):
        kafedra = Kafedra.objects.create(name="Backend", faculty=self.faculty)
        self.assertEqual(str(kafedra), "CS - Backend")


class GradeModelTest(TestCase):

    def setUp(self):
        _, _, _, subject, group = make_base_data()
        user = User.objects.create_user(username="student1", password="pass1234")
        self.student = Student.objects.create(user=user, group=group)
        self.subject = subject

    def test_grade_created(self):
        grade = Grade.objects.create(
            student=self.student, subject=self.subject, rating=8, semester=1
        )
        self.assertEqual(grade.rating, 8)
        self.assertEqual(grade.semester, 1)

    def test_grade_str(self):
        grade = Grade.objects.create(
            student=self.student, subject=self.subject, rating=7, semester=2
        )
        self.assertIn("student1", str(grade))
        self.assertIn("7", str(grade))

    def test_grade_add_rating_method(self):
        grade = Grade.objects.create(
            student=self.student, subject=self.subject, rating=5, semester=3
        )
        grade.add_rating(9)
        grade.refresh_from_db()
        self.assertEqual(grade.rating, 9)

    def test_grade_add_rating_invalid_raises(self):
        grade = Grade.objects.create(
            student=self.student, subject=self.subject, rating=5, semester=4
        )
        with self.assertRaises(ValueError):
            grade.add_rating(11)
        with self.assertRaises(ValueError):
            grade.add_rating(-1)

    def test_grade_unique_together(self):
        Grade.objects.create(
            student=self.student, subject=self.subject, rating=6, semester=1
        )
        with self.assertRaises(Exception):
            Grade.objects.create(
                student=self.student, subject=self.subject, rating=8, semester=1
            )



class ServiceTest(TestCase):

    def setUp(self):
        _, _, self.kafedra, _, self.group = make_base_data()
        self.user = User.objects.create_user(username="testuser", password="pass1234")

    def test_create_teacher_success(self):
        teacher = create_teacher(self.user, self.kafedra)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.user, self.user)

    def test_create_teacher_duplicate_raises(self):
        create_teacher(self.user, self.kafedra)
        with self.assertRaises(ValueError):
            create_teacher(self.user, self.kafedra)

    def test_create_student_success(self):
        student = create_student(self.user, self.group)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.user, self.user)

    def test_create_student_duplicate_raises(self):
        create_student(self.user, self.group)
        with self.assertRaises(ValueError):
            create_student(self.user, self.group)

    def test_student_cannot_become_teacher(self):
        create_student(self.user, self.group)
        with self.assertRaises(ValueError):
            create_teacher(self.user, self.kafedra)

    def test_teacher_cannot_become_student(self):
        create_teacher(self.user, self.kafedra)
        with self.assertRaises(ValueError):
            create_student(self.user, self.group)



class PermissionTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.uni, self.faculty, self.kafedra, self.subject, self.group = make_base_data()

        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.regular_user = User.objects.create_user(username="regular", password="pass1234")

        teacher_user = User.objects.create_user(username="teacher1", password="pass1234")
        self.teacher = create_teacher(teacher_user, self.kafedra)

        student_user = User.objects.create_user(username="student1", password="pass1234")
        self.student = create_student(student_user, self.group)

    def test_anyone_can_get_universities(self):
        response = self.client.get("/api/v1/university/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_university(self):
        response = self.client.post("/api/v1/university/", {"name": "NewUni", "country": "KZ"})
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_regular_user_cannot_create_university(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post("/api/v1/university/", {"name": "NewUni", "country": "KZ"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_university(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/v1/university/", {"name": "NewUni", "country": "KZ"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_can_create_grade(self):
        self.client.force_authenticate(user=self.teacher.user)
        data = {
            "student": self.student.id,
            "subject": self.subject.id,
            "rating": 8,
            "semester": 1,
        }
        response = self.client.post("/api/v1/grade/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_grade(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            "student": self.student.id,
            "subject": self.subject.id,
            "rating": 8,
            "semester": 1,
        }
        response = self.client.post("/api/v1/grade/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_sees_only_own_grades(self):
        other_user = User.objects.create_user(username="other", password="pass1234")
        other_student = create_student(other_user, self.group)

        Grade.objects.create(student=self.student, subject=self.subject, rating=7, semester=1)
        Grade.objects.create(student=other_student, subject=self.subject, rating=9, semester=1)

        self.client.force_authenticate(user=self.student.user)
        response = self.client.get("/api/v1/grade/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["rating"], 7)

    def test_admin_sees_all_grades(self):
        other_user = User.objects.create_user(username="other2", password="pass1234")
        other_student = create_student(other_user, self.group)

        Grade.objects.create(student=self.student, subject=self.subject, rating=7, semester=1)
        Grade.objects.create(student=other_student, subject=self.subject, rating=9, semester=1)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/grade/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)



class UniversityCRUDTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.client.force_authenticate(user=self.admin)

    def test_create_university(self):
        response = self.client.post("/api/v1/university/", {"name": "MIT", "country": "USA"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(University.objects.count(), 1)

    def test_list_universities(self):
        University.objects.create(name="MIT", country="USA")
        University.objects.create(name="Stanford", country="USA")
        response = self.client.get("/api/v1/university/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_single_university(self):
        uni = University.objects.create(name="MIT", country="USA")
        response = self.client.get(f"/api/v1/university/{uni.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "MIT")

    def test_update_university(self):
        uni = University.objects.create(name="MIT", country="USA")
        response = self.client.patch(f"/api/v1/university/{uni.id}/", {"country": "UK"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uni.refresh_from_db()
        self.assertEqual(uni.country, "UK")

    def test_delete_university(self):
        uni = University.objects.create(name="MIT", country="USA")
        response = self.client.delete(f"/api/v1/university/{uni.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(University.objects.count(), 0)

    def test_search_university_by_name(self):
        University.objects.create(name="MIT", country="USA")
        University.objects.create(name="Oxford", country="UK")
        response = self.client.get("/api/v1/university/?search=MIT")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "MIT")


class GradeCRUDTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        _, _, self.kafedra, self.subject, self.group = make_base_data()

        teacher_user = User.objects.create_user(username="teacher1", password="pass1234")
        self.teacher = create_teacher(teacher_user, self.kafedra)
        self.client.force_authenticate(user=self.teacher.user)

        student_user = User.objects.create_user(username="student1", password="pass1234")
        self.student = create_student(student_user, self.group)

    def test_create_grade(self):
        data = {"student": self.student.id, "subject": self.subject.id, "rating": 8, "semester": 1}
        response = self.client.post("/api/v1/grade/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)

    def test_update_grade(self):
        grade = Grade.objects.create(
            student=self.student, subject=self.subject, rating=5, semester=1
        )
        response = self.client.patch(f"/api/v1/grade/{grade.id}/", {"rating": 9})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        grade.refresh_from_db()
        self.assertEqual(grade.rating, 9)

    def test_delete_grade(self):
        grade = Grade.objects.create(
            student=self.student, subject=self.subject, rating=5, semester=1
        )
        response = self.client.delete(f"/api/v1/grade/{grade.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Grade.objects.count(), 0)

    def test_filter_grade_by_semester(self):
        Grade.objects.create(student=self.student, subject=self.subject, rating=7, semester=1)
        Grade.objects.create(student=self.student, subject=self.subject, rating=9, semester=2)
        response = self.client.get("/api/v1/grade/?semester=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)