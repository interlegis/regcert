from django.contrib import admin

from core.models import Enrollment, Student, Course, Certificate

# Register your models here.
admin.site.register(Enrollment)
admin.site.register(Certificate)
admin.site.register(Course)
admin.site.register(Student)
