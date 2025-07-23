# coordinador/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Retorna el valor de un diccionario para una clave dada.
    Útil para acceder a elementos en plantillas.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None # Retorna None si no es un diccionario