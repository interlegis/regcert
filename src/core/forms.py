from django import forms

from core.models import Course, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fiels = ['name', 'birthday', 'nationality', 'rg']


class StudentCoursesForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False)
