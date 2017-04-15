from django.template import Template, Context
from django.http import HttpResponse

template = Template("""
<img src="/static/logo.png" />
<ul>
{% for thing in thingies %}
<li>{{ thing }}
{% endfor %}
</ul>
""")

def index(request):
    thingies = ['list', 'of', 'things']
    context = Context(dict(thingies=thingies)) 
    return HttpResponse(template.render(context))
