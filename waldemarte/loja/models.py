from django.db import models
from .classes.frete import calcula_frete
import json
# Create your models here. -> informacoes que vamos armazenar no BD

# TODO : creio que alguns campos precisam ter certas constraints, precisa ser ajustado, exemplo not empty
# TODO :por default todos os campos sao NOT NULL, alguns precisam ser nullable, corrigir conforme necessario
# TODO : implementar metodos de asdict() ou to_json() para as classe, para poder mandar via http


# Usuario abstrato, serve como base do vendedor e comprador
class AbstractUsuario(models.Model):
    nome = models.CharField(max_length=20)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, null=True)
    cpf = models.CharField(max_length=15, null=True)
    senha = models.CharField(max_length=254, null=True) # TODO : implementar autenticacao
    # Transacoes : Classe implementada (One to Many)
    class Meta:
        abstract = True

    def asdict(self):
        return {
            "nome" : self.nome,
            "email" : self.email,
            "telefone" : self.telefone,
            "cpf" : self.cpf
        }
    
    @classmethod
    def authenticate(cls, email, senha) -> models.Model | None:
        user = cls.objects.get(email = email)
        if user.senha == senha:
            return user
        else:
            return None



# Classe Vendedor
class Vendedor(AbstractUsuario):
    cnpj = models.CharField(max_length=254, null=True)
    # Produtos : Implementado como ForeignKey da classe Produto (One to Many)
    banco_agencia = models.CharField(max_length=254, null=True)
    banco_conta = models.CharField(max_length=254, null=True)

    def asdict(self):
        return {
           "cnpj" : self.cnpj ,
           "id" : self.id
        } + super.asdict()
# Classe comprador
class Comprador(AbstractUsuario):
    # Lista de cartoes : Implementado como Foreign Key (One to Many)
    # Endereco : Foreign Key da class Endereco (One to Many)
    pass
    def __str__(self):
        return f"{self.nome}|{self.email}|{self.telefone}|{self.cpf}|{self.senha}"

    def asdict(self):
        return super().asdict() + {
            "id" : self.id,
            "endereco" : [end.asdict() for end in self.endereco_set]
            }


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

    def asdict(self):
        return {
            "cep" : self.cep,
            "rua" : self.rua,
            "bairro" : self.bairro,
            "cidade" : self.cidade,
            "estado" : self.estado,
            "numero" : self.numero,
            "complemento" : self.complemento,
        }



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
            "id" : self.id,
            "nome" : self.nome,
            "preco" : self.preco,
            "opcoes" : [str(op) for op in self.opcao_set.all()],
            "especificacoes" : self.especificacoes,
            "estoque" : self.estoque,
            "vendedor" : self.vendedor.nome
        }
    def to_json(self):
        return json.dumps(self.asdict())
    
# Imagem de um produto
class ImagemProduto(models.Model):
    img_url = models.CharField(max_length=254)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)



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


    

class CarrinhoDeCompras(models.Model):
    # Relacao Many to Many para incluir lista de produtos
    produtos = models.ManyToManyField(Produto)
    # TODO : implementar contagem de produtos, nao testei para entender se a 
    # relacao many to many permite repeticao, se sim, descartar esse todo
    comprador =  models.ForeignKey(Comprador, on_delete=models.CASCADE, default=1)
    preco_final = models.FloatField(default=0.0)

    def to_json(self):
        return json.dumps({
            "user_id" : self.comprador_id,
            "produtos" : [p.asdict() for p in self.produtos.all()],
            "preco_final" : self.preco_final,
            "frete" : calcula_frete(self)
        })
    
    def clear(self):
        for prod in self.produtos.all():
            self.produtos.remove(prod)
            prod.carrinhodecompras_set.remove(self)
            prod.save()
        self.save()


# Registro de vendas, referencia vendedor produto e comprador como foreign Key
class Transacao(models.Model):
    comprador = models.ForeignKey(Comprador, null=True,  on_delete=models.SET_NULL)
    produto = models.ForeignKey(Produto, null=True, on_delete=models.SET_NULL)
    preco = models.FloatField()
    vendedor = models.ForeignKey(Vendedor, null=True, on_delete=models.SET_NULL)



    @staticmethod
    def registrar_carrinho(carrinho : CarrinhoDeCompras):
        for prod in carrinho.produtos.all():
            Transacao(
                comprador_id=carrinho.comprador_id,
                vendedor_id=prod.vendedor_id,
                produto_id=prod.id,
                preco=prod.preco
            ).save()
            


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