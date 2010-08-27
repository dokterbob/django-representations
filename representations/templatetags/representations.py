import logging

from django.template import loader, Node, TemplateSyntaxError
from django import template
from django.template.context import Context

register = template.Library()

def get_representation_content(model, representation, context=None):
    opts = model._meta
    template_list = [ "representations/%s/%s/%s" % (opts.app_label, opts.object_name.lower(), representation), 
                      "representations/%s/%s"    % (opts.app_label, representation), ]
                      
    logging.debug("Representing the %s '%s' as %s." % (opts.object_name.lower(), model, representation))
    
    t = loader.select_template(template_list)

    if context is None:
        context = Context()
        
    return t.render(context)
    
class RepresentNode(Node):
    def __init__(self, model_name, model_exp, representation_exp):
        self.model_name = model_name
        self.model_exp = model_exp
        self.representation_exp = representation_exp

    def render(self, context):
        model = self.model_exp.resolve(context)
        representation = self.representation_exp.resolve(context)
        
        try:
            opts = model._meta
        except AttributeError:
            raise TemplateSyntaxError("%s is not a model" % (self.model_name,))


        return get_representation_content(model, representation, context=context)

                                
def do_represent(parser, token):
    """
    This tag takes a model and passes it and the context to
    a template in the following location:
    
    representations/app_label/object_name/[template] or
    representations/app_label/[template] or
    representations/[template] (whichever comes first)
    {% represent [model] as "[template]" %}

    This allows you to have the same representation for the object in numerous
    templates.

    This also allows you to have a list of mixed content types and if they all have
    representation templates made, you display them all in the same list.

    For instance you can have a list of videos, photes, blog entries and news stories
    and if all of them has a representation of "summary.html" you could make a single
    list of all the objects.
    """
    bits = token.contents.split()
    try:
        assert len(bits) == 4 and bits[2] == 'as', "Tag format is: {%% %s [model] as [template_name] %%}" % (bits[0])
    except AssertionError, e:
        raise TemplateSyntaxError(str(e))
    
    return RepresentNode(bits[1],
                         parser.compile_filter(bits[1]),
                         parser.compile_filter(bits[3])
                         )

register.tag('represent', do_represent)
