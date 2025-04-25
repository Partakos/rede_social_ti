import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField()
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True, default=None)
    data_nascimento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome_completo

class Publicacao(models.Model):
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='publicacoes/', blank=True, null=True)
    video = models.FileField(upload_to='publicacoes_videos/', blank=True, null=True)
    data_publicacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-data_publicacao']
    
    def __str__(self):
        return f"Publicação de {self.autor.nome_completo}"
    
    def delete(self, *args, **kwargs):
        if self.imagem:
            if os.path.isfile(self.imagem.path):
                os.remove(self.imagem.path)
        if self.video:
            if os.path.isfile(self.video.path):
                os.remove(self.video.path)
        super().delete(*args, **kwargs)

class Amizade(models.Model):
    remetente = models.ForeignKey(Perfil, related_name='remetente', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Perfil, related_name='destinatario', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    ), default='pendente')
    data_solicitacao = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['remetente', 'destinatario']
    
    def __str__(self):
        return f"{self.remetente} para {self.destinatario} - {self.status}"