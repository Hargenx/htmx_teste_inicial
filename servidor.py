import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))


import lista
from bottle import TEMPLATE_PATH, debug, redirect, request, route, run, template

TEMPLATE_PATH.append(DIR)


@route("/")
def index():
    '''Pega as vitimas listadas.'''
    try:
        vitima = lista.obter_todas_listas()
        contagem = lista.contar_vitimas()
        return template("index", vitima=vitima, contagem=contagem)
    except:
        return template("erro")
    
@route("/adicionar", method="POST")
def adicionar():
    '''Adiciona uma nova vitima a lista.'''
    try:
        nome = request.forms.get("nome")
        if nome:
            lista.adicionar_vitima(nome)
        redirect("/")
    except:
        return template("erro")

@route('/set_status_lista', method="POST")
def set_status_lista():
    '''Altera o status de uma vitima.'''
    try:
        vitima = lista.obter_todas_listas()
        contagem = lista.contar_vitimas()
        vitima_id = int(request.forms.get("vitima_id"))
        status = request.forms.get("status")
        if status == "true":
            status = True
        else:
            status = False
        lista.set_status_vitima(vitima_id, status)
        redirect("/")
    except:
        return template("erro")
    


@route('/apagar/<id:int>', method="GET")
def apagar(id):
    '''Apaga uma vitima da lista.'''
    try:
        lista.apagar_vitima(id)
        redirect("/")
    except:
        return template("erro")
    
if __name__ == "__main__":
    debug(True)
    run(host="localhost", port=8080, reloader=True)