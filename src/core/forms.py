from django import forms
from django.utils.translation import ugettext as _

from core.models import Course, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fiels = ['name', 'birthday', 'nationality', 'rg']


class StudentCoursesForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('courses')
    )


class InvalidateCertificateForm(forms.Form):
    reason = forms.CharField(widget = forms.Textarea)


class SearchCertificateForm(forms.Form):

    options = (
        ('validation_code', 'Validation Code'),
        ('name', 'Name'),
    )

    search_options = forms.ChoiceField(widget=forms.RadioSelect, choices=options)
    search_text = forms.CharField(max_length=40)
