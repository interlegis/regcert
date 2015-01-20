from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext as _

from baco import Baco, base16


class Student(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    birthday = models.DateField(verbose_name=_('birthday'))
    nationality = models.CharField(max_length=40,
                                   verbose_name=_('nationality'))
    rg = models.CharField(max_length=15, verbose_name=_('rg'))
    registration_date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    duration = models.IntegerField(verbose_name=_('duration'))
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end date'))

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, verbose_name=_('student'))
    course = models.ForeignKey(Course, verbose_name=_('course'))

    class Meta:
        verbose_name = _('Enrollment')
        verbose_name_plural = _('Enrollments')

    def __str__(self):
        return '{}# {} - {}'.format(self.id, self.course.name,
                                    self.student.name)


class Certificate(models.Model):
    enrollment = models.ForeignKey(Enrollment, verbose_name=_('enrollment'))
    verification_code = models.CharField(max_length=32, unique=True,
                                         verbose_name=_('verification code'))
    date_time = models.DateTimeField(verbose_name=_('date/time'))

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')

    def save(self, *args, **kwargs):
        uuid = uuid4()
        self.verification_code = Baco.to_62(uuid.hex, base16)
        super(Certificate, self).save(*args, **kwargs)
