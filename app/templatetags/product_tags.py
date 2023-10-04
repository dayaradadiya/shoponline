from django import template

register = template.Library()

@register.simple_tag
def call_sellprice(price,discount):
    if discount is None or discount is 0:
        return price
    elif price == '' or  discount == '':
        return
    sellprice = price
    sellprice = round(price - (sellprice * discount/100),2)
    return sellprice
  

