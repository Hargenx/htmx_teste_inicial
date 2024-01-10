from __future__ import unicode_literals
import logging
import sqlite3
import tempfile
from pathlib import Path


caminho_db = Path(tempfile.gettempdir()) / "lista.db"
conn = sqlite3.connect(str(caminho_db))
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS lista (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        feito BOOL NOT NULL
        )"""
)
conn.commit()


def criar_lista(nome):
    """Adciona uma nova vitima para lista na base de dados e retorna a mesma"""
    try:
        c.execute("INSERT INTO lista (nome, feito) VALUES (?, 0)", (nome,))
        conn.commit()
        return {"id": c.lastrowid, "nome": nome, "feito": False}
    except Exception as e:
        logging.error(f"Erro ao criar lista: {e}")
        return {"erro": f"Erro ao criar lista: {e}"}
    
def set_status_lista(id, feito):
    '''Define se a lista está feita, ou vai ser e retorna ela parcialmente'''
    try:
        c.execute("UPDATE lista SET feito=? WHERE id=?", (feito, id))
        conn.commit()
        return {"id": id, "feito": feito}
    except Exception as e:
        logging.error(f"Erro ao atualizar status da lista: {e}")
        return {"erro": f"Erro ao atualizar status da lista: {e}"}
    
def apagar_lista(id):
    '''Apagar uma vitima apagada :devil: '''
    try:
        c.execute('DELETE FROM lista WHERE id=?', (id,))
        conn.commit()
    except Exception as e:
        logging.error(f"Erro ao apagar lista: {e}")
        return {"erro": f"Erro ao apagar lista: {e}"}
    
def obter_todas_vitimas():
    """Retorna todas as listas"""
    try:
        return c.execute("SELECT * FROM lista ORDER BY id").fetchall()
    except Exception as e:
        logging.error(f"Erro ao obter todas as listas: {e}")
        return {"erro": f"Erro ao obter todas as listas: {e}"}
    

def obter_vitimas_por_lista(id):
    """Retorna todas as vitimas de uma lista"""
    try:
        return c.execute("SELECT * FROM lista WHERE lista_id =? ORDER BY id", (id,)).fetchone()
    except Exception as e:
        logging.error(f"Erro ao obter todas as vitimas da lista: {e}")
        return {"erro": f"Erro ao obter todas as vitimas da lista: {e}"}
    
def contar_vitimas():
    """Retorna a quantidade de vitimas e a quantidade de vitimas que ainda não foram tratadas"""
    try:
        c.execute("SELECT COUNT(*) FROM lista")
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM lista WHERE feito")
        feito = c.fetchone()[0]
        return {'feito': feito, 'total': total}
    except Exception as e:
        logging.error(f"Erro ao contar vitimas: {e}")
        return {"erro": f"Erro ao contar vitimas: {e}"}
    