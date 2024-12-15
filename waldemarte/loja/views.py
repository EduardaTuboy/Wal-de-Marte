from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from .classes.frete import calcula_frete
from django.contrib import messages

import json

import loja.classes.notificacoes as notif
from .models import *


# Create your views here. -> interacao que o usuario tem no frontend vem pra ca


# Documentacao dos inputs e outputs das funcoes estao no urls.py


# TODO : index,
#        fazer autenticaçao de senha
def index(request):
    query = request.GET.get("query", "")  # Obtém o termo de busca
    produtos = Produto.objects.all()  # Produtos padrão

    # Se houver uma busca, filtra os produtos
    if query:
        produtos = produtos.filter(nome__icontains=query)

    context = {
        "produtos": produtos,
        "query": query  # Passa o termo de busca para reutilizar no template
    }
    return render(request, "index.html", context)
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
         
        # Autenticacao feita, nao se ao certo qq precisa p login
        user = Comprador.authenticate(email, senha)
        # user = {} # usuario dummy

        if user is not None:
            #login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Login invalido")
            return render(request, "login.html")
    # se a requisiçao for GET, retorna a pagina de login
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "register.html")

        Comprador(
            nome=request.POST.get("username"),
            email=email,
            senha=password
        ).save()
    return render(request, "register.html")

# TODO : verificacao mais robusta nas funcoes de criacao
def criar_comprador(request : HttpRequest):
    args = json.loads(request.body) 
    try:
        user = Comprador(**args)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    user.save()
    return HttpResponse()

def comprador_set_endereco(request : HttpRequest):
    args = json.loads(request.body)
    try:
        addr = Endereco(comprador = Comprador.objects.get(id=args["id"]),**args["endereco"])
        addr.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    return HttpResponse()

def comprador_add_cartao(request : HttpRequest):
    args = json.loads(request.body)
    try:
        cartao = Cartao(comprador = Comprador.objects.get(id=args["id"]), **args["cartao"])
        cartao.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    return HttpResponse()
        

def get_comprador(request : HttpRequest, id):
    try:
        user = Comprador.objects.get(pk=id)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(user.asdict), content_type="application/json")

def update_comprador(request : HttpRequest):
    args = json.loads(request.body)
    try:
        updated_user = Comprador.objects.get(pk=args["id"])
        for field, value in args["fields"].items():
            setattr(updated_user, field, value)
        updated_user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest
    return HttpResponse()

def criar_vendedor(request : HttpRequest):
    args = json.loads(request.body)
    try:
        user = Vendedor(**args)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    user.save()
    return HttpResponse()

def update_vendedor(request : HttpRequest):
    args = json.loads(request.body)
    try:
        updated_user = Vendedor.objects.get(pk=args["id"])
        for field, value in args["fields"].items():
            setattr(updated_user, field, value)
        updated_user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest
    return HttpResponse()
    

def get_vendedor(request : HttpRequest, id):
    try:
        user = Vendedor.objects.get(pk=id)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(user.asdict), content_type="application/json")

def add_produto(request : HttpRequest):
    args = json.loads(request.body)
    try:
        owner = Vendedor.objects.get(pk=args["id"])
        produto = Produto(vendedor = owner, **args["produto"])
        produto.save()
        opcoes = [Opcao(opcao=op, produto=produto) for op in args["opcoes"]]
        for op in opcoes:
            op.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse()

def get_produto(request : HttpRequest, id):
    try: 
        prod = Produto.objects.get(pk=id)


        if request.headers.get("Content-Type") == "application/json":
            # Retorna o produto como JSON se for chamado via API
            return HttpResponse(json.dumps(prod.asdict()), content_type="application/json")

        # Se não for JSON, renderiza um template HTML
        return render(request, "produto.html", {"produto": prod})

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def update_produto(request : HttpRequest):
    args = json.loads(request.body)
    try:
        updated_produto = Produto.objects.get(pk=args["id"])
        for field, value in args["fields"].items():
            if field != "opcoes":
                setattr(updated_produto, field, value)
        for op in args["fields"]["opcoes"]:
            updated_produto.opcao_set.add(Opcao(opcao=op))
        updated_produto.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest
    return HttpResponse()
    



def query_produtos(request: HttpRequest):
    args = json.loads(request.body) if request.method == "POST" else {}
    produtos = []
    try:
        # Se argumentos existirem, faz a busca
        produtos = Produto.objects.filter(
            nome__icontains=args.get("query", ""), 
            preco__gte=args.get("preco_lim_inf", 0),
            preco__lte=args.get("preco_lim_sup", 999999)
        )
    except Exception as e:
        print(e)
        if request.method == "POST":
            return HttpResponseBadRequest("Invalid input")
    if request.method == "POST":
        produtos_json = [p.to_json() for p in produtos]
        return HttpResponse(json.dumps(produtos_json), content_type="application/json")
    return produtos  # Retorna os objetos diretamente se chamado internamente




def get_cart(request : HttpRequest):
    return HttpResponse(CarrinhoDeCompras.objects.get(comprador_id=json.loads(request.body)["user_id"]).to_json(),
                        content_type="application/json")

def add_to_cart(request : HttpRequest):
    args = json.loads(request.body)
    user = Comprador.objects.get(pk=args["user_id"])
    new_produto = Produto.objects.get(pk=args["produto_id"])
    cart = None
    try:
        cart = CarrinhoDeCompras.objects.get(comprador_id=args["user_id"])
    except CarrinhoDeCompras.DoesNotExist as e:
        cart = CarrinhoDeCompras(comprador = user)
    cart.save()
    cart.produtos.add(new_produto)
    cart.preco_final += new_produto.preco
    cart.save()
    return HttpResponse(json.dumps({"novo_frete" : calcula_frete(cart),
                                    "novo_preco" : cart.preco_final
                                    }),
                                    content_type="application/json")

def remove_from_cart(request : HttpRequest):
    args = json.loads(request.body)
    user = Comprador.objects.get(pk=args["user_id"])
    produto = Produto.objects.get(pk=args["produto_id"])
    cart = CarrinhoDeCompras.objects.get(comprador_id=args["user_id"]) 
    cart.produtos.remove(produto)
    produto.carrinhodecompras_set.remove(cart)
    cart.preco_final -= produto.preco
    cart.save()
    produto.save()
    return HttpResponse(json.dumps({"novo_frete" : calcula_frete(cart),
                                    "novo_preco" : cart.preco_final
                                    }),
                                    content_type="application/json")


    




def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])



def comprar_carrinho(request, user_id):
    carrinho = CarrinhoDeCompras.objects.filter(comprador_id = user_id)[0]
    transacoes = Transacao.registrar_carrinho(carrinho)
    carrinho.clear()
    # Nao eh mto elegangte para varios produtos, mas funciona
    for t in transacoes:
        notif.notificarCompraComprador(t)
        notif.notificarCompraVendedor(t)


