from django import forms
from .models import Perfil, Publicacao

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome_completo', 'email', 'foto', 'data_nascimento', 'biografia']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'biografia': forms.Textarea(attrs={'rows': 4}),
        }

class PublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['conteudo', 'imagem', 'video']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que você está pensando?'}),
        }