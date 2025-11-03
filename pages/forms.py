from django import forms


class PingForm(forms.Form):
    domain = forms.CharField(
        label='Домен',
        max_length=253,
        widget=forms.TextInput(attrs={'placeholder': 'example.com'}),
    )

    def clean_domain(self):
        domain = self.cleaned_data['domain'].strip()
        if not domain:
            raise forms.ValidationError('Enter a domain name or IP address.')

        if domain.startswith(('http://', 'https://')):
            domain = domain.split('://', 1)[1]
        domain = domain.split('/', 1)[0]

        if not domain:
            raise forms.ValidationError('Enter a valid domain without protocol.')

        return domain
