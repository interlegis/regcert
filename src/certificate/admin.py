from django.contrib import admin

from certificate.models import Certificate, InvalidCertificate

# Register your models here.
admin.site.register(Certificate)
admin.site.register(InvalidCertificate)
