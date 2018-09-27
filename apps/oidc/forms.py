from django import forms
from oauth2_provider.forms import AllowForm


class NonceAllowForm(AllowForm):
    nonce = forms.CharField(required=False, widget=forms.HiddenInput())
