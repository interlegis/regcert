from uuid import uuid4

from django.db import models

from baco import Baco, base16


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
    verification_code = models.CharField(max_length=32, unique=True)
    date_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        uuid = uuid4()
        self.verification_code = Baco.to_62(uuid.hex, base16)
        super(Certificate, self).save(*args, **kwargs)
