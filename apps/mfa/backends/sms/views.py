from django.views.generic.edit import FormView
from apps.mfa import verify


class CodeView(FormView):
    template_name = 'contact.html'
    form_class = CodeForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        device = SMSCode.objects.get(
            code=data,
            device__user=user,
            expires__gt=timezone.now()).device

        verify(self.request, device)
        return super().form_valid(form)


class CodeForm(forms.Form):
    code = forms.CharField()

    def clean_code(self):
        data = self.cleaned_data['code']
        if not SMSCode.objects.filter(
            code=data,
            device__user=user,
            expires__gt=timezone.now()).exists():
                raise forms.ValidationError("Incorrect code!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
