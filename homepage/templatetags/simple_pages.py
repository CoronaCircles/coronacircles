from django import template

from homepage.models import SimplePage

register = template.Library()


class SimplePageNode(template.Node):
    def __init__(self, context_name):
        self.context_name = context_name

    def render(self, context):
        pages = SimplePage.objects.all()
        context[self.context_name] = pages
        return ""


@register.tag
def get_pages(parser, token):
    """Get all simple pages

    Example:
        {% get_pages as pages %}"""
    bits = token.split_contents()
    if bits[-2] != "as":
        raise template.TemplateSyntaxError("Usage: {% get_pages as pages %}")
    context_name = bits[-1]
    return SimplePageNode(context_name)
