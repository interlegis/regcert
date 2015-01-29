from django import forms
from django.utils.translation import ugettext as _
from django.db import IntegrityError

from core.models import Certificate, Course, Enrollment, Student


class InvalidateCertificateForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label=_('Reason'))


class SearchCertificateForm(forms.Form):

    options = (
        ('verification_code', _('Verification code')),
        ('name', _('Name')),
    )

    search_options = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=options)
    search_text = forms.CharField(max_length=40)


class ValidateCertificateForm(forms.Form):
    verification_code = forms.CharField(max_length=22,
        label=_('validation code'))


class CertificateCreateForm(forms.ModelForm):

    student_rg = forms.CharField(max_length=40, label=_('Student rg'))
    course = forms.CharField(max_length=40, label=_('Course'))
    enrollment = forms.CharField(max_length=100, label=_('Enrollment'))

    class Meta:
        model = Certificate
        fields = ['certificate_number', 'book_number', 'book_sheet',
            'book_date', 'book_date', 'process_number', 'executive_director',
            'educational_secretary']

    def save(self, commit=True):
        student_rg = self.cleaned_data['student_rg']
        course_name = self.cleaned_data['course']
        enrollment = self.cleaned_data['enrollment']

        try:
            student = Student.objects.get(rg=student_rg)
        except Student.DoesNotExist as e:
            raise e

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist as e:
            raise e

        enrollment = Enrollment(student=student, course=course,
            enrollment=enrollment)
        try:
            enrollment.save()
        except IntegrityError as e:
            pass

        if Certificate.objects.filter(enrollment__student__rg=student_rg,
            enrollment__course__name=course_name):
            raise
        instance = super(CertificateCreateForm, self).save(commit=False)
        instance.enrollment = enrollment

        if commit:
            instance.save()
        return instance
