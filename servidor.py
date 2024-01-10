import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))


import lista
from bottle import TEMPLATE_PATH, debug, redirect, request, route, run, template

TEMPLATE_PATH.append(str(DIR))


@route("/")
def index():
    '''Pega as vitimas listadas.'''
    try:
        listas = lista.obter_todas_vitimas()
        contagem = lista.contar_vitimas()
        return template("index", listas=listas, contagem=contagem)
    except Exception as e:
        print(f"Erro: {e}")
        raise e
    
@route("/adicionar", method="POST")
def adicionar():
    '''Adiciona uma nova vitima a lista.'''
    try:
        nome = request.forms.get("nome")
        if nome:
            lista.criar_lista(nome)
        return index()
    except Exception as e:
        print(f"Erro na rota '/': {e}")
        raise e

@route('/set_status_lista', method="POST")
def set_status_lista():
    '''Altera o status de uma vitima.'''
    try:
        todas_vitimas = lista.obter_todas_vitimas()
        id_acoes_feitas = set(int(id) for id in request.forms.getall('vitima'))
        for vitima in todas_vitimas:
            novo_status = vitima['id'] in id_acoes_feitas
            lista.set_status_lista(vitima['id'], novo_status)
        #redirect("/") - Cai no except, não acheio o pq...
        return index()
    except Exception as e:
        print(f"Erro na rota '/': {e}")
        raise e
    


@route('/apagar/<id:int>', method="GET")
def apagar(id):
    '''Apaga uma vitima da lista.'''
    try:
        lista.apagar_lista(id)
        return index()
    except Exception as e:
        print(f"Erro na rota '/': {e}")
        raise e


if __name__ == "__main__":
    debug(True)
    run(host="127.0.0.1", port=8080, reloader=True)