from flask import render_template as render_template


class TemplateProvider:
    EMAIL_ACTIVATE_TPL = 'email/activate.html'
    
    def __init__(self, render_template_engine):
        self.render_template_engine = render_template_engine
        
    def render_template(self, template, **kwargs):
        return self.render_template_engine(template, **kwargs)


template_provider = TemplateProvider(render_template)
