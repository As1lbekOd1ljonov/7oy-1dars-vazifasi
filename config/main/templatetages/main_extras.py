from django import template
from ..models import Brands, Color, Cars

register = template.Library()

@register.simple_tag
def send_all_brands():
    return Brands.objects.all()

@register.simple_tag
def send_all_colors():
    return Color.objects.all()

@register.simple_tag
def send_all_cars():
    return Cars.objects.all()