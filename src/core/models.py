from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=40)
    birthday = models.DateField()
    nationality = models.CharField(max_length=40)
    rg = models.CharField(max_length=15)
    registration_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=40)
    hours = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)

    def __str__(self):
        return '{}# {} - {}'.format(self.id, self.course.name,
                                    self.student.name)


class Certificate(models.Model):
    enrollment = models.ForeignKey(Enrollment)
    date_time = models.DateTimeField()
