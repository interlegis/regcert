from django.contrib import admin

from core.models import Student, Course, Certificate

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Certificate)
