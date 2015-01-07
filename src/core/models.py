from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=40)
    birthday = models.DateField()
    nationality = models.CharField(max_length=40)
    rg = models.CharField(max_length=15)
    registration_date_time = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    name = models.CharField(max_length=40)
    hours = models.IntegerField()
    begin = models.DateField()
    end = models.DateField()


class Enrollment(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)


class Certificate(models.Model):
    enrolment = models.ForeignKey(Enrollment)
    date_time = models.DateTimeField()
