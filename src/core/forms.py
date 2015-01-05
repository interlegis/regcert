from django import forms

from core.models import Student


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
