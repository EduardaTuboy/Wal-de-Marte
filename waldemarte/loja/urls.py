from django.urls import path

from . import views

urlpatterns = [
    # TODO: index
    path("", views.index, name="index"),  # Página inicial


    #Página de login
    path("login/", views.login, name="login"),            


    path("register/", views.register, name="register"),

    path("perfil/", views.perfil, name="perfil"),

    path("compra/", views.compra, name="compra"),



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

    # Retorna comprador por id
    # Json (response) -> {"nome", "email", "telefone", "cpf", "endereco" : []}
    path("user/get-comprador/<int:id>", views.get_comprador),
    
    # Altera dados de comprador por id (nao altera endereco ou cartoes)
    # Json (request) -> {"id", "fields" : {<nome_do_campo>}}
    # Siga o modelo em user/save-comprador para nome do campo
    path("user/comprador-edit", views.update_comprador),

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

    # Edita vendedor, mesma coisa do comprador-edit
    path("user/vendedor-edit", views.update_vendedor),

    # Retorna um vendedor por id
    path("user/get-vendedor/<int:id>", views.get_vendedor),

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
        # "imagens" : [<urls>],
        # "opcoes" :[<opcoes>]    
    # }
    path("produto/add-produto", views.add_produto),

    path("produto/delete/<int:p_id>", views.delete_produto),

    # Funciona igual os de editar usuario
    # Porem "opcoes" dentro de "fileds" deve ser uma lista
    path("produto/produto-edit", views.update_produto),

    # Retorna um produto por id
    path("produto/<int:id>", views.get_produto, name="get_produto"),


    # Retorna uma busca por produtos, limitada por nome e preco
    # Json (request) -> {"query", "preco_lim_inf", "preco_lim_sup"}
    # Json (response) -> {"nome", "preco", "opcoes" : [lista de strings], "especificacoes", "estoque", "vendedor"}
    path("produto/query-produtos", views.query_produtos),

    # Retorna o carrinho de compras de um usuario
    # Json (request) -> {"user_id"}
    # Json (response) -> {
    #   "user_id", "preco_final", "frete",
    #   "produtos" : [{"nome", "preco", "opcoes" : [lista de strings], "especificacoes", "estoque", "vendedor"}]
    # }
    path("cart", views.get_cart, name="get_cart"),


    # Adiciona um produto ao carrinho do usuario
    # Json (request) -> {"user_id", "produto_id"}
    # Json (responde) -> {"novo_frete", "novo_preco"}
    path("cart/add", views.add_to_cart),

    # Remove um produto do carrinho do usuario
    # Json (request) -> {"user_id", "produto_id"}
    # Json (responde) -> {"novo_frete", "novo_preco"}
    path("cart/remove", views.remove_from_cart),



    # IMPORTANATE: este endpoint sera criado desconsiderando qualque logica de pagamento, 
    # apenas para poder implenetar outras partes que dependem de compra, 
    # nem sei se vamos implementar uma logica mais complexa, mas fica o aviso
    # Json (request) -> {"user_id"}, Nao rpecisa dos produtos, o sistema pega o carrinho de compras direto

    path("comprar-carrinho/<int:user_id>", views.comprar_carrinho),


    # O id de usuario sera puxado da session
    path("comprar-produto/<int:produto_id>", views.comprar_produto)
]   