from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
#from django.shorcuts import render

def login(request):

    document = get_template('login.html')
    """
    document = open("D:/BOTS-PYTHON/botFacebook/botFacebook/views/login.html")
    template = Template(document.read())
    document.close()
    """    

    #context = Context()
    #login = template.render(context)
    login = document.render()

    return HttpResponse(login)
    #return render(request, "login.html")