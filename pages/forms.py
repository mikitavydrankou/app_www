from django import forms


class PentestForm(forms.Form):
    OPERATION_CHOICES = [
        ('ping', 'Ping — check host availability'),
        ('port_scan', 'Port Scan — scan open ports'),
        ('dns_lookup', 'DNS Lookup — retrieve DNS records'),
        ('http_headers', 'HTTP Headers — fetch HTTP headers'),
    ]
    
    target = forms.CharField(
        label='Target (domain or IP)',
        max_length=253,
        widget=forms.TextInput(attrs={
            'placeholder': 'example.com or 192.168.1.1',
            'style': 'width: 100%;'
        }),
    )
    
    operations = forms.MultipleChoiceField(
        label='Select operations',
        choices=OPERATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text='Select one or more operations',
    )
    
    ports = forms.CharField(
        label='Ports to scan (optional)',
        max_length=100,
        required=False,
        initial='80,443,22,21,25',
        widget=forms.TextInput(attrs={
            'placeholder': '80,443,22,21,25',
            'style': 'width: 100%;'
        }),
        help_text='Used only for Port Scan',
    )

    def clean_target(self):
        target = self.cleaned_data['target'].strip()
        if not target:
            raise forms.ValidationError('Enter target.')

        if target.startswith(('http://', 'https://')):
            target = target.split('://', 1)[1]
        target = target.split('/', 1)[0]

        return target
    
    def clean_ports(self):
        ports = self.cleaned_data.get('ports', '').strip()
        if not ports:
            return '80,443,22,21,25'  # default
        
        try:
            port_list = [p.strip() for p in ports.split(',')]
            for port in port_list:
                port_num = int(port)
                if not 1 <= port_num <= 65535:
                    raise ValueError
        except ValueError:
            raise forms.ValidationError('Enter valid port numbers separated by commas (1-65535).')
        
        return ports
