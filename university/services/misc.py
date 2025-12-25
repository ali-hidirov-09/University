from university.models import Teacher, Student

def create_teacher(target_user, kafedra):
    if Student.objects.filter(user=target_user).exists():
        raise ValueError("Student teacher bo‘la olmaydi")

    if Teacher.objects.filter(user=target_user).exists():
        raise ValueError("Teacher allaqachon bor")

    teacher = Teacher.objects.create(user=target_user, kafedra=kafedra)
    return teacher


def create_student(target_user, group):
    if Student.objects.filter(user=target_user).exists():
        raise ValueError("Student allaqachon bor")

    if Teacher.objects.filter(user=target_user).exists():
        raise ValueError("Teacher student bo'la olmaydi")

    student= Student.objects.create(user=target_user, group=group)
    return student



