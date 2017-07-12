from django import template


register = template.Library()

@register.inclusion_tag('form-horizontal.html',          
                        takes_context=True)                                               
def bootstrap_form_horizontal(                                                     
        context, form, size_left=2, size_right=8, button=None,                     
        fold_class='sm'):                                                          
    return dict(                                                                   
        form=form,                                                                 
        size_left=size_left,                                                       
        size_right=size_right,                                                     
        button=button,                                                             
        fold_class=fold_class,                                                     
        )