from django.db import models

# Create your models here. -> informacoes que vamos armazenar no BD



# Usuario abstrato, serve como base do vendedor e comprador
class AbstractUsuario(models.Model):
    nome = models.CharField(max_length=20)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=15)
    # TODO: Lista de transacoes, requer classe transacao primeiro
    class Meta:
        abstract = True

# Classe Vendedor
class Vendedor(AbstractUsuario):
    cnpj = models.CharField(max_length=254)
    # Produtos : Implementado como ForeignKey da classe Produto (One to Many)
    banco_agencia = models.CharField(max_length=254)
    banco_conta = models.CharField(max_length=254)


# Classe comprador
class Comprador(AbstractUsuario):
    # Lista de cartoes : Implementado como Foreign Key Many to One
    pass

# Classe do cartao, para o comprador
class Cartao(models.Model):
    numero = models.CharField(max_length=254)
    cvv = models.CharField(max_length=3)
    # One to Many : lista de cartoes do comprador
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE)



class Produto(models.Model):
    nome = models.CharField(max_length=254)
    preco = models.FloatField()
    # TODO : avaliacoes, requer classe avaliacao
    # opcoes : implementado como foreign key na classe Opcao (One to Many)
    especificacoes = models.TextField()
    estoque = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)



# Poduto contem uma lista de opcoes, o melhor jeito de implementa-la eh com uma table separada (Many to One)
class Opcao(models.Model):
    opcao = models.CharField(max_length=254)
    # Many to One : lista de opcoes do produto
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)





