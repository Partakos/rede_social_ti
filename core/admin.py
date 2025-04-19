from django.contrib import admin
from .models import Perfil, Publicacao, Amizade

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'usuario', 'email')
    search_fields = ('nome_completo', 'usuario__username', 'email')

@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('autor', 'conteudo_curto', 'data_publicacao')
    list_filter = ('data_publicacao', 'autor')
    search_fields = ('conteudo', 'autor__nome_completo')
    
    def conteudo_curto(self, obj):
        return obj.conteudo[:50] + '...' if len(obj.conteudo) > 50 else obj.conteudo
    conteudo_curto.short_description = 'Conteúdo'

@admin.register(Amizade)
class AmizadeAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'status', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('remetente__nome_completo', 'destinatario__nome_completo')