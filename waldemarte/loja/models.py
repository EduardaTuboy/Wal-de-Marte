from django.db import models

# Create your models here. -> informacoes que vamos armazenar no BD



class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.FloatField()
    # TODO : avaliacoes, requer classe avaliacao
    # opcoes : implementado como foreign key na classe Opcao
    especificacoes = models.TextField()
    estoque = models.IntegerField()



# Poduto contem uma lista de opcoes, o melhor jeito de implementa-la eh com uma table separada (One to Many)
class Opcao(models.Model):
    opcao = models.CharField(max_length=255)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)



class Usuario(models.Model):
    nome = models.CharField(max_length=20)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=15)
    # TODO: Lista de transacoes, requer classe transacao primeiro



