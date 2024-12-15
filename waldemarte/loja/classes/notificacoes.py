from ..models import *
import smtplib
from email.message import EmailMessage



# fodase toma ae a senha
gmail_app_password = "arar iuki dtvb kztj"
my_email = "waldemarteloja@gmail.com"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("waldemarteloja@gmail.com", gmail_app_password)


def notificarCompraVendedor(compra : Transacao):
    message = f"Sua venda do produto {compra.produto.nome} foi confirmada no valor de R${compra.preco:.2f}\n"
    message += f"O produto deve ser entregue no endereço: {compra.comprador.endereco_set.all()[0].asdict()}"
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Compra confirmada"
    msg["From"] = my_email
    msg["To"] = compra.comprador.email
    server.send_message(msg)


def notificarCompraComprador(compra : Transacao):
    message = f"Sua compra do produto {compra.produto.nome} foi confirmada no valor de R${compra.preco:.2f}\n"
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Compra confirmada"
    msg["From"] = my_email
    msg["To"] = compra.comprador.email
    server.send_message(msg)    
        