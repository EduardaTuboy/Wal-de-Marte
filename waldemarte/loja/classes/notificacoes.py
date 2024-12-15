from ..models import *
import smtplib, ssl


def notificarCompraVendedor(compra : Transacao):
    pass


def notificarCompraComprador(compra : Transacao):
    with smtplib.SMTP_SSL():
        pass