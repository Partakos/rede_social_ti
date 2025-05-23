# Generated by Django 5.1.6 on 2025-04-19 13:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='perfis/')),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('biografia', models.TextField(blank=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='publicacoes/')),
                ('video', models.FileField(blank=True, null=True, upload_to='publicacoes_videos/')),
                ('data_publicacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.perfil')),
            ],
            options={
                'ordering': ['-data_publicacao'],
            },
        ),
        migrations.CreateModel(
            name='Amizade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('recusado', 'Recusado')], default='pendente', max_length=20)),
                ('data_solicitacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinatario', to='core.perfil')),
                ('remetente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remetente', to='core.perfil')),
            ],
            options={
                'unique_together': {('remetente', 'destinatario')},
            },
        ),
    ]
