from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<int:perfil_id>/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('amigos/solicitar/<int:perfil_id>/', views.solicitar_amizade, name='solicitar_amizade'),
    path('amigos/aceitar/<int:solicitacao_id>/', views.aceitar_amizade, name='aceitar_amizade'),
    path('publicar/', views.criar_publicacao, name='criar_publicacao'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)