from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from .classes.frete import calcula_frete_produto, calcula_frete_carrinho
from .classes.db_init import initDefaultDB
from django.contrib import messages
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json

import loja.classes.notificacoes as notif
from .models import *


# Create your views here. -> interacao que o usuario tem no frontend vem pra ca


# Documentacao dos inputs e outputs das funcoes estao no urls.py


# TODO : index,
#        fazer autenticaçao de senha





def index(request : HttpRequest):
    if Produto.objects.exists():
        initDefaultDB()
    query = request.GET.get("query", "")  # Obtém o termo de busca
    produtos = Produto.objects.all()  # Produtos padrão
    user = request.session.get("user", None)     # Se houver uma busca, filtra os produtos
    if query:
        produtos = produtos.filter(nome__icontains=query)

    context = {
        "produtos": produtos,
        "user" : user, # se autenticado eh o user, senao eh none,
        "query": query  # Passa o termo de busca para reutilizar no template
    }
    return render(request, "index.html", context)
    

def login(request : HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
         
        # Autenticacao feita, nao se ao certo qq precisa p login
        user = Comprador.authenticate(email, senha)

        if user is not None:
            #login(request, user)
            context = {
                "user" : user.id
            }
            request.session["user"] = model_to_dict(user)
            return redirect("index")
        else:
            messages.error(request, "Login invalido")
            return redirect(request, "login.html")
    # se a requisiçao for GET, retorna a pagina de login
    messages.error(request, "")
    return render(request, "login.html")


def register(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "register.html")

        c = Comprador(
            nome=request.POST.get("username"),
            email=email,
            senha=password
        )
        c.save()
        Endereco.default(c).save()
        request.session["user"] = model_to_dict(c)
        return redirect("index")
    messages.error(request, "")
    return render(request, "register.html")



def perfil(request : HttpRequest):
    user = request.session.get("user", None)
    
    if user is None:
        return redirect("login")
    
    request.session["user"] = None
    return redirect("index")


def carrinho(request : HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")
    return render(request, "carrinho.html", {"user" : user})


def compra(request : HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")
    return render(request, "compra.html", {"user" : user})

def vendaConcluida(request : HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")
    return render(request, "vendaConcluida.html", {"user" : user})

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
        imagens = [ImagemProduto(img_url=i, produto=produto) for i in args["imagens"]]
        for op in opcoes:
            op.save()
        for i in imagens:
            i.save()
    except Exception as e:
        print(e.with_traceback())
        return HttpResponseBadRequest()
    return HttpResponse()

def delete_produto(request, p_id):
    Produto.objects.get(pk=p_id).delete()
    return HttpResponse()

def get_produto(request: HttpRequest, id):
    try:
        prod = Produto.objects.get(pk=id)
        if request.headers.get("Content-Type") == "application/json":
            # Retorna o produto como JSON se for chamado via API
            return HttpResponse(json.dumps(prod.asdict()), content_type="application/json")

        # Se não for JSON, renderiza um template HTML
        user = request.session.get("user", None)
        if user is not None:
            user = Comprador.objects.get(pk=user["id"])
            try:
                return render(request, "produto.html", {"produto": prod, "frete": calcula_frete_produto(user, prod)})
            except Exception as inner_e:
                return render(request, "produto.html", {"produto": prod, "frete": "Cadastre endereço para ver seu frete."})
        return render(request, "produto.html", {"produto": prod, "frete": "Login para ver seu frete."})

    except Exception as e:
        # Substitua .with_traceback() por apenas imprimir ou lidar com a exceção
        print(e)  # Você pode registrar o erro no console
        return HttpResponseBadRequest("Erro ao buscar produto")



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


def get_cart(request: HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")

    try:
        cart = CarrinhoDeCompras.objects.get(comprador_id=user["id"])
        produtos = cart.produtos.all()
    except CarrinhoDeCompras.DoesNotExist:
        produtos = []

    try:
        context = {
            "user": user,
            "produtos": produtos,
            "preco_final": cart.preco_final if produtos else 0,
            "frete": calcula_frete_carrinho(cart) if produtos else 0
        }
    except:
        context = {
            "user": user,
            "produtos": produtos,
            "preco_final": cart.preco_final if produtos else 0,
            "frete": "Registre endereco para ver frete"
        }
    return render(request, "carrinho.html", context)

def add_to_cart(request: HttpRequest):
    if request.method == "POST":
        try:
            # Verifica se o usuário está logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")
            
            # Obtém o comprador logado
            user = Comprador.objects.get(pk=session_user["id"])
            
            # Obtém o produto pelo ID do formulário
            produto_id = request.POST.get("produto_id")
            produto = Produto.objects.get(pk=produto_id)
            
            # Tenta obter ou criar o carrinho do usuário
            cart, created = CarrinhoDeCompras.objects.get_or_create(comprador=user)
            
            # Adiciona o produto ao carrinho
            cart.produtos.add(produto)
            cart.preco_final += produto.preco
            cart.save()

            # Mensagem de sucesso
            messages.success(request, f"Produto '{produto.nome}' foi adicionado ao carrinho!")
            return redirect("get_cart")  # Redireciona para a página do carrinho

        except Produto.DoesNotExist:
            return HttpResponseBadRequest("Produto não encontrado.")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Erro ao adicionar produto ao carrinho.")
    else:
        return HttpResponseBadRequest("Método não permitido.")


def remove_from_cart(request: HttpRequest):
    if request.method == "POST":
        try:
            # Obtém o usuário logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")
            
            # Obtém o comprador
            user = Comprador.objects.get(pk=session_user["id"])
            
            # Obtém o carrinho do comprador
            cart = CarrinhoDeCompras.objects.get(comprador=user)
            
            # Obtém o produto a ser removido
            produto_id = request.POST.get("produto_id")
            produto = Produto.objects.get(pk=produto_id)
            
            # Remove o produto do carrinho
            cart.produtos.remove(produto)
            cart.preco_final -= produto.preco
            cart.save()

            messages.success(request, f"Produto '{produto.nome}' removido do carrinho.")
            return redirect("get_cart")  # Redireciona de volta para o carrinho

        except (Produto.DoesNotExist, CarrinhoDeCompras.DoesNotExist):
            return HttpResponseBadRequest("Produto ou carrinho não encontrado.")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Erro ao remover produto do carrinho.")
    else:
        return HttpResponseBadRequest("Método não permitido.")

def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])

def compra_carrinho(request: HttpRequest):
    if request.method == "POST":
        try:
            # Verifica se o usuário está logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")
            
            # Obtém os IDs dos produtos do formulário
            produtos_ids = request.POST.getlist("produtos_ids")
            produtos = Produto.objects.filter(pk__in=produtos_ids)

            # Verifica se os produtos existem
            if not produtos.exists():
                return HttpResponseBadRequest("Produtos não encontrados.")

            # Calcula o total dos produtos
            total = sum(produto.preco for produto in produtos)

            # Renderiza a página de compra com os produtos e o total
            return render(request, "compra.html", {"produtos": produtos, "total": total})

        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Erro ao processar a compra.")
    else:
        return redirect("index")


def comprar_produto(request: HttpRequest, produto_id):
    try:
        produto = Produto.objects.get(pk=produto_id)
        session_user = request.session.get("user", None)
        if session_user is None:
            return redirect("login")
        
        # Passa o produto para a página de compra
        total = produto.preco
        return render(request, "compra.html", {"produtos": [produto], "total": total})


    except Produto.DoesNotExist:
        return HttpResponseBadRequest("Produto não encontrado.")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Erro ao acessar página de compra.")

def realizar_compra(request: HttpRequest):
    if request.method == "POST":
        try:
            # Verifica se o usuário está logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")

            # Obtém os IDs dos produtos do formulário
            produtos_ids = request.POST.getlist("produtos_ids")  # Lista de IDs enviada
            
            # Log para depuração
            print("Produtos enviados (lista):", produtos_ids)

            # Verifica se a lista de IDs está vazia
            if not produtos_ids:
                return HttpResponseBadRequest("Nenhum produto foi selecionado para compra.")

            # Filtra os produtos com base nos IDs
            produtos = Produto.objects.filter(pk__in=produtos_ids)
            
            # Verifica se os produtos foram encontrados
            if not produtos.exists():
                return HttpResponseBadRequest("Nenhum produto correspondente encontrado no banco de dados.")

            # Obtém o comprador
            user = Comprador.objects.get(pk=session_user["id"])

            # Registra transações para cada produto
            for produto in produtos:
                print(f"Processando produto: {produto.nome} (ID: {produto.id})")
                try:
                    transacao = Transacao.registrar_produto(user, produto)
                    print("Transação registrada com sucesso.")
                except Exception as e:
                    print(f"Erro ao registrar transação para o produto {produto.id}: {e}")
                    raise e
                try:
                    notif.notificarCompraComprador(transacao)
                    notif.notificarCompraVendedor(transacao)
                    print("Notificações enviadas com sucesso.")
                except Exception as e:
                    print(f"Erro ao enviar notificações para o produto {produto.id}: {e}")
                    raise e

            # Redireciona para a página de venda concluída
            return redirect("vendaConcluida")

        except Comprador.DoesNotExist:
            return redirect("login")
        except Exception as e:
            print("Erro durante a compra:", e)
            return HttpResponseBadRequest("Erro ao realizar a compra.")
    else:
        return redirect("index")
