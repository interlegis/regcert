from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext as _

from audit_log.models.fields import CreatingUserField, LastUserField
from baco import Baco, base16



class Student(models.Model):
    name = models.CharField(_('name'), max_length=40)
    birthday = models.DateField(_('birthday'))
    nationality = models.CharField(_('nationality'), max_length=40)
    rg = models.CharField(_('rg'), max_length=15)
    registration_date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(_('name'), max_length=40)
    duration = models.IntegerField(_('duration'))
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, verbose_name=_('student'))
    course = models.ForeignKey(Course, verbose_name=_('course'))
    enrollment = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = (('enrollment', 'student', 'course'),)
        verbose_name = _('Enrollment')
        verbose_name_plural = _('Enrollments')

    def __str__(self):
        return '#{} {}'.format(self.enrollment, self.course.name)


class Certificate(models.Model):
    enrollment = models.ForeignKey(Enrollment, verbose_name=_('enrollment'),
                                   unique=True)
    verification_code = models.CharField(_('verification code'), max_length=32,
                                         unique=True)
    certificate_number = models.CharField(_('certificate number'),
                                          max_length=50, unique=True)

    book_number = models.IntegerField(_('book number'))
    book_sheet = models.IntegerField(_('book sheet'))
    book_date = models.DateField(_('book date'))
    process_number = models.IntegerField(_('process number'))
    executive_director = models.CharField(_('executive director'),
                                          max_length=40)
    educational_secretary = models.CharField(_('educational secretary'),
                                             max_length=40)

    # ato de credenciamento

    created_by = CreatingUserField(related_name="created_certificate")
    date_time = models.DateTimeField(auto_now_add=True)

    invalidated = models.BooleanField(default=False)
    invalidated_by = LastUserField()
    invalidated_reason = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')

    def save(self, *args, **kwargs):
        if not self.verification_code:
            uuid = uuid4()
            while Certificate.objects.filter(verification_code==uuid):
                uuid = uuid4()
            self.verification_code = Baco.to_62(uuid.hex, base16)
        super(Certificate, self).save(*args, **kwargs)
