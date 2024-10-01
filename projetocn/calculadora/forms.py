from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BisseccaoForm(forms.Form):
    funcao = forms.CharField(label='Função', max_length=100)
    limite_esquerdo = forms.IntegerField(label='Extremo Esquerdo')
    limite_direito = forms.IntegerField(label='Extremo Direito')
    tolerancia = forms.FloatField(label='Tolerância')
    iteracoes = forms.IntegerField(label='Número de Interações')

    def __init__(self, *args, **kwargs):
        super(BisseccaoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Resolver'))

class NewtonForm(forms.Form):
    funcao = forms.CharField(label='Função f(x)', max_length=100)
    derivada = forms.CharField(label='Derivada f\'(x)', max_length=100)
    valor_inicial = forms.FloatField(label='Valor Inicial')
    tolerancia = forms.FloatField(label='Tolerância')
    iteracoes = forms.IntegerField(label='Número de Iterações', initial=100)

class FalsaPosicaoForm(forms.Form):
    funcao = forms.CharField(label='Função f(x)', max_length=200)
    intervalo_inferior = forms.FloatField(label='Intervalo Inferior (a)')
    intervalo_superior = forms.FloatField(label='Intervalo Superior (b)')
    tolerancia = forms.FloatField(label='Tolerância')
    max_iteracoes = forms.IntegerField(label='Máximo de Iterações')

class SecanteForm(forms.Form):
    funcao = forms.CharField(label='Função', max_length=100, required=True)
    x0 = forms.FloatField(label='Valor de x0', required=True)
    x1 = forms.FloatField(label='Valor de x1', required=True)
    tolerancia = forms.FloatField(label='Tolerância', required=True)
    max_iteracoes = forms.IntegerField(label='Máximo de Iterações', required=True)