from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext as _

from audit_log.models.fields import CreatingUserField
from baco import Baco, base16


class CertificateBase(models.Model):

    # Certificate data

    verification_code = models.CharField(_('verification code'), max_length=32,
                                         unique=True)
    verification_code_date_time = models.DateTimeField(auto_now_add=True)
    book_number = models.IntegerField(_('book number'))
    book_sheet = models.IntegerField(_('book sheet'))
    book_date = models.DateField(_('book date'))
    process_number = models.IntegerField(_('process number'))
    executive_director = models.CharField(_('executive director'),
                                          max_length=40)
    educational_secretary = models.CharField(_('educational secretary'),
                                             max_length=40)

    # Course data

    course_name = models.CharField(_('name'), max_length=40)
    course_duration = models.IntegerField(_('duration'))
    course_start_date = models.DateField(_('start date'))
    course_end_date = models.DateField(_('end date'))

    # Student data

    student_name = models.CharField(_('name'), max_length=40)
    student_birthday = models.DateField(_('birthday'))
    student_nationality = models.CharField(_('nationality'), max_length=40)
    student_rg = models.CharField(_('rg'), max_length=15)

    class Meta:
        abstract = True
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')


class Certificate(CertificateBase):
    certificate_number = models.CharField(_('certificate number'),
                                          max_length=50, unique=True)
    created_by = CreatingUserField(related_name="created_certificate")

    def save(self, *args, **kwargs):
        if not self.verification_code:
            uuid = uuid4()
            while Certificate.objects.filter(verification_code=uuid):
                uuid = uuid4()

            self.verification_code = Baco.to_62(uuid.hex, base16)
        super(Certificate, self).save(*args, **kwargs)


class InvalidCertificate(CertificateBase):
    certificate_number = models.CharField(_('certificate number'),
                                          max_length=50)
    created_by = CreatingUserField(related_name="created_certificate_invalid")
    invalidated_by = CreatingUserField(related_name="invalidated_certificate")
    invalidated_reason = models.TextField()
