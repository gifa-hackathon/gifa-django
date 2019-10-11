from django import forms
from django.utils.translation import gettext_lazy as _

from odkcollect.models import ODKConnector

class ODKConnectorAdminForm(forms.ModelForm):
    db_password = forms.CharField(
        widget=forms.PasswordInput,
        label=_('DB Password')
    )
    class Meta:
        model = ODKConnector
        fields = '__all__'
