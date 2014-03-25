from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def url_active(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return "active"
    return "request.path: {req}, urls: {url}".format(
            req=request.path,
            url=", ".join(reverse(url) for url in urls.split())
        )

@register.filter
def remove_uncomplete_latex(text):
    # Even number of segments separated by $$ means uncomplete
    # display equation
    if len(text.split('$$')) % 2 == 0:
        # Return the original text
        return '$$'.join(text.split('$$')[:-1])
    elif len(text.split('$')) % 2 == 0:
        return '$'.join(text.split('$')[:-1])
    else:
        return text

class DefineNode(template.Node):
    def __init__(self, name, nodelist):
        self.name = name
        self.nodelist = nodelist

    def __repr__(self):
        return "<DefineNode>"

    def render(self, context):
        context[self.name] = self.nodelist.render(context)
        return ''

@register.tag
def define(parser, token):
    """
    Adds a name to the context for referencing an arbitrarily defined block
    of template code.

    For example:

        {% define my_block %}
        This is the content.
        {% enddefine %}

    Now anywhere in the template:

        {{ my_block }}
    """

    bits = list(token.split_contents())

    if len(bits) != 2:
        raise TemplateSyntaxError("Expected format is: {% define variable %}")

    name = bits[1]
    nodelist = parser.parse(('enddefine',))
    parser.delete_first_token()

    return DefineNode(name, nodelist)
