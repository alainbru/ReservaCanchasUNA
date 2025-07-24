from django import template
from models import Reserva

register = template.Library()

#filtra la reserva por dia y hora
@register.filter
def get_reserva(reservas, dia_hora):
    dia, hora = dia_hora
    return reservas.filter(dia=dia, hora=hora).first()