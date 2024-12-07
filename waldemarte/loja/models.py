from django.db import models

import json
# Create your models here. -> informacoes que vamos armazenar no BD

# TODO : creio que alguns campos precisam ter certas constraints, precisa ser ajustado, exemplo not empty
# TODO :por default todos os campos sao NOT NULL, alguns precisam ser nullable, corrigir conforme necessario

# Usuario abstrato, serve como base do vendedor e comprador
class AbstractUsuario(models.Model):
    nome = models.CharField(max_length=20)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=15)
    senha = models.CharField(max_length=254) # TODO : implementar autenticacao
    # Transacoes : Classe implementada (One to Many)
    class Meta:
        abstract = True

# Classe Vendedor
class Vendedor(AbstractUsuario):
    cnpj = models.CharField(max_length=254, null=True)
    # Produtos : Implementado como ForeignKey da classe Produto (One to Many)
    banco_agencia = models.CharField(max_length=254, null=True)
    banco_conta = models.CharField(max_length=254, null=True)


# Classe comprador
class Comprador(AbstractUsuario):
    # Lista de cartoes : Implementado como Foreign Key (One to Many)
    # Endereco : Foreign Key da class Endereco (One to Many)
    pass
    def __str__(self):
        return f"{self.nome}|{self.email}|{self.telefone}|{self.cpf}|{self.senha}"

# Classe do cartao, para o comprador
class Cartao(models.Model):
    numero = models.CharField(max_length=254)
    cvv = models.CharField(max_length=3)
    # One to Many : lista de cartoes do comprador
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE, default=1)

# Classe para endereco do comprador
class Endereco(models.Model):
    cep = models.CharField(max_length=254)
    rua = models.CharField(max_length=254)
    bairro = models.CharField(max_length=254)
    cidade = models.CharField(max_length=254)
    estado = models.CharField(max_length=254)
    numero = models.CharField(max_length=254)
    complemento = models.CharField(max_length=254)
    # Many to One : enderecoes cadastrados para comprador
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE, default=1)



# Classe do produto
class Produto(models.Model):
    nome = models.CharField(max_length=254)
    preco = models.FloatField()
    # avaliacoes : Foreign Key (Onne to Many) na classe Avaliacao
    # opcoes : implementado como foreign key na classe Opcao (One to Many)
    especificacoes = models.TextField()
    estoque = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=1)

    def asdict(self):
        return {
            "nome" : self.nome,
            "preco" : self.preco,
            "opcoes" : [str(op) for op in self.opcao_set],
            "especificacoes" : self.especificacoes,
            "estoque" : self.estoque,
            "vendedor" : self.vendedor.nome
        }
    def to_json(self):
        return json.dumps(self.asdict())

# Poduto contem uma lista de opcoes, o melhor jeito de implementa-la eh com uma table separada (Many to One)
class Opcao(models.Model):
    opcao = models.CharField(max_length=254)
    # Many to One : lista de opcoes do produto
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.opcao

# Avaliacao do produto
class Avaliacao(models.Model):
    comentario = models.TextField()
    nota = models.SmallIntegerField() # TODO : adicionar constraint de nota de 1 a 5
    # Many to one : produto com lista de avaliacoes
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)
    # Many to One : comprador tem suas avaliacoes 
    comprador = models.ForeignKey(Comprador, null=True, on_delete=models.SET_NULL)
    # Data da avaliacao gerada automaticamente
    data = models.DateField(auto_now_add=True)


# Registro de vendas, referencia vendedor produto e comprador como foreign Key
class Transacao(models.Model):
    comprador = models.ForeignKey(Comprador, null=True,  on_delete=models.SET_NULL)
    produto = models.ForeignKey(Produto, null=True, on_delete=models.SET_NULL)
    preco = models.FloatField()
    vendedor = models.ForeignKey(Vendedor, null=True, on_delete=models.SET_NULL)

class CarrinhoDeCompras(models.Model):
    # Relacao Many to Many para incluir lista de produtos
    produtos = models.ManyToManyField(Produto)
    # TODO : implementar contagem de produtos, nao testei para entender se a 
    # relacao many to many permite repeticao, se sim, descartar esse todo
    comprador =  models.ForeignKey(Comprador, on_delete=models.CASCADE, default=1)
    preco_final = models.FloatField()


class Notificacao(models.Model):
    # Django nao permite uma foreign key referenciando classe abstrata
    # logo, dois campos serao criados
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE, null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True)
    # Classe enum para status de notificacao
    class NotificacaoStatus(models.TextChoices):
        # Caso seja necessario, implementar novos codigos de erro, verificar documentacao do django para fazer certinho
        SUCESSO = "OK", "SUCESSO"
        ERRO = "ERR", "ERRO"
        ERRO_DB = "DB_ERR", "ERRO_ACESSO_DB"
    status = models.CharField(max_length=254, choices=NotificacaoStatus)
    mensagem = models.TextField()