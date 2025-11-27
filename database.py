# database.py
import json
import os

def carregar_json(nome_arquivo):
    """
    Carrega dados de um arquivo JSON.
    Retorna um dicionário vazio se o arquivo não existir.
    """
    if not os.path.exists(nome_arquivo):
        return {}
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Aviso: O arquivo {nome_arquivo} estava corrompido. Um novo será criado.")
        return {}
    except Exception as e:
        print(f"Erro ao carregar {nome_arquivo}: {e}")
        return {}

def salvar_json(nome_arquivo, dados):
    """
    Salva dados em um arquivo JSON.
    """
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar {nome_arquivo}: {e}")
        return False