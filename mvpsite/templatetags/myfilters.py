from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='addplaceholder')
def addclass(value, arg):
    return value.as_widget(attrs={'class':"form-control", 'placeholder': arg})