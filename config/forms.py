from django import forms
from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = '__all__'
        widgets = {
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'atividade': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'obs': forms.Textarea(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control'}),
        }