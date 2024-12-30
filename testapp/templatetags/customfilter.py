from django import template
register=template.Library()


@register.filter
def sum_field(data, field_name):
   total = 0
   for item in data:
      if isinstance(item, dict):
         total += item.get(field_name, 0)
      elif isinstance(item, list):
         for subitem in item:
            if isinstance(subitem, dict):
               total += subitem.get(field_name, 0)
   return total


def subtraction(value,s):
   val = value - s
   return val

register.filter('sub',subtraction)

def addition(value,s):
   val = value + s
   return val

register.filter('add',addition)