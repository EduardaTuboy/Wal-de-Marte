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
    path("user/save-comprador", views.criar_comprador),

    # Retorna compradores em uma string, apenas para debug
    path("user/comprador-all", views.return_compradores),


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
    path("user/save-vendedor", views.criar_vendedor),

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
    path("user/set-endereco-comprador", views.comprador_set_endereco),


    # Salva um cartao associado a um comprador
    # Body do request em json ->
    # {
    #     "id" : <user_id>,
    #     "cartao" : {
    #         "numero" : <numero>,
    #         "cvv" : <cvv>
    #     }

    # }
    path("user/add-cartao-comprador", views.comprador_add_cartao),

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
    path("user/add-produto", views.add_produto),



    # Retorna uma busca por produtos, limitada por nome e preco
    # Json (request) -> {"query", "preco_lim_inf", "preco_lim_sup"}
    # Json (response) -> {"nome", "preco", "opcoes" : [lista de strings], "especificacoes", "estoque", "vendedor"}
    path("query-produtos", views.query_produtos)

]   