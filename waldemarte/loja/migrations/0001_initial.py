# Generated by Django 5.1.4 on 2024-12-14 20:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comprador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=15)),
                ('senha', models.CharField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254)),
                ('preco', models.FloatField()),
                ('especificacoes', models.TextField()),
                ('estoque', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=15)),
                ('senha', models.CharField(max_length=254)),
                ('cnpj', models.CharField(max_length=254, null=True)),
                ('banco_agencia', models.CharField(max_length=254, null=True)),
                ('banco_conta', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=254)),
                ('cvv', models.CharField(max_length=3)),
                ('comprador', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.comprador')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=254)),
                ('rua', models.CharField(max_length=254)),
                ('bairro', models.CharField(max_length=254)),
                ('cidade', models.CharField(max_length=254)),
                ('estado', models.CharField(max_length=254)),
                ('numero', models.CharField(max_length=254)),
                ('complemento', models.CharField(max_length=254)),
                ('comprador', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.comprador')),
            ],
        ),
        migrations.CreateModel(
            name='Opcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opcao', models.CharField(max_length=254)),
                ('produto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.produto')),
            ],
        ),
        migrations.CreateModel(
            name='CarrinhoDeCompras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco_final', models.FloatField(default=0.0)),
                ('comprador', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.comprador')),
                ('produtos', models.ManyToManyField(to='loja.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('nota', models.SmallIntegerField()),
                ('data', models.DateField(auto_now_add=True)),
                ('comprador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.comprador')),
                ('produto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.FloatField()),
                ('comprador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.comprador')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.produto')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.vendedor')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='vendedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loja.vendedor'),
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('OK', 'SUCESSO'), ('ERR', 'ERRO'), ('DB_ERR', 'ERRO_ACESSO_DB')], max_length=254)),
                ('mensagem', models.TextField()),
                ('comprador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loja.comprador')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loja.vendedor')),
            ],
        ),
    ]