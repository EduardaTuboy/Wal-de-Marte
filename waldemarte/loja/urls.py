from django.urls import path

from . import views

urlpatterns = [
    # TODO: index
    path("", views.index),

    # Salva um comprador na base de dados
    # Body do request em json -> 
    # {
    #   "nome" : <nome>,
    #   "email" : <email>,
    #   "telefone" : <telefone>,
    #   "cpf" : <cpf>,
    #   "senha" : <senha>
    #}
    path("comprador/salvar", views.criar_comprador),

    # Retorna compradores em uma string, apenas para debug
    path("comprador/all", views.return_compradores),


    # Salva um vendedor na base de dados
    # Body do request em json -> 
    # {
    #   "nome" : <nome>,
    #   "email" : <email>,
    #   "telefone" : <telefone>,
    #   "cpf" : <cpf>,
    #   "senha" : <senha>,
    #   "cnpj" : <cnpj>
    #   "banco_conta" : <conta>,
    #   "banco_agencia" : <agencia>
    #}
    path("vendedor/salvar", views.criar_vendedor),

    # Salva o endereco para um comprador pelo ID
    # Body do request em json -> 
    # {
    #     "id" : <user_id>,
    #     "endereco" : {
    #         "cep" :<cep>,
    #         "rua" : <rua>,
    #         "bairro" : <bairro>,
    #         "cidade" : <cidade>,
    #         "estado" : <estado>,
    #         "numero" : <numero>,
    #         "complemento" : <complemento>
    #     }
    # }
    path("comprador/set-endereco", views.comprador_set_endereco),


    # Salva um cartao associado a um comprador
    # Body do request em json ->
    # {
    #     "id" : <user_id>,
    #     "cartao" : {
    #         "numero" : <numero>,
    #         "cvv" : <cvv>
    #     }

    # }
    path("comprador/add-cartao", views.comprador_add_cartao),

    # Adiciona produto associado a um vendedor
    # Json -> 
    # {
        # "id" : <vendedor_id>,
        # "produto" : {
        #     "nome" : <nome>,
        #     "preco" : <preco>,
        #     "especificacoes" : <specs>,
        #     "estoque" : <init_estoque>
        # },
        # "opcoes" :[<opcoes>]    
    # }
    path("vendedor/add-produto", views.add_produto),


    # TODO : testar
    # Retorna uma busca por produtos, limitada por nome e preco
    # Json (request) -> {"query", "preco_lim_inf", "preco_lim_sup"}
    # Json (response) -> {"nome", "preco", "opcoes" : [lista de strings], "especificacoes", "estoque", "vendedor"}
    path("produtos/busca")

]   