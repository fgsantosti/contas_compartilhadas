from django import forms
from .models import Grupo, Renda, Gasto

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao']

class RendaForm(forms.ModelForm):
    class Meta:
        model = Renda
        fields = ['valor', 'descricao', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['valor', 'descricao', 'fixo', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }


class AdicionarMembroForm(forms.Form):
    email = forms.EmailField(label='E-mail do usuário', max_length=100)

    from django import forms


class FiltrarGastosForm(forms.Form):
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data Início"
    )
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data Fim"
    )
