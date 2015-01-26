from django import forms
from django.utils.translation import ugettext as _


class InvalidateCertificateForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label=_('Reason'))


class SearchCertificateForm(forms.Form):

    options = (
        ('validation_code', _('Validation code')),
        ('name', _('Name')),
    )

    search_options = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=options)
    search_text = forms.CharField(max_length=40)


class ValidateCertificateForm(forms.Form):
    validation_code = forms.CharField(max_length=5, label=_('validation code'))
