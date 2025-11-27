# gamedata.py

"""
Armazena todos os dados estáticos do jogo.
"""

# Dados do planeta inicial
DADOS_TERRA_MAE = {
    "nome": "Terra-Mãe",
    "prod_base": 1,
    "custo_base_upgrade": 10,
    "imagem_path": "planeta_base.png" # A imagem principal
}

# Lista de planetas que podem ser colonizados
LISTA_PLANETAS_COLONIZAVEIS = [
    {
        "nome": "Colônia de Marte",
        "prod_base": 5,
        "custo_base_upgrade": 50,
        "imagem_path": "planeta_marte.png"
    },
    {
        "nome": "Minas de Europa",
        "prod_base": 20,
        "custo_base_upgrade": 250,
        "imagem_path": "planeta_europa.png"
    },
    {
        "nome": "Refinaria de Titã",
        "prod_base": 80,
        "custo_base_upgrade": 1200,
        "imagem_path": "planeta_tita.png"
    },
    {
        "nome": "Posto de Kepler-186f",
        "prod_base": 300,
        "custo_base_upgrade": 5000,
        "imagem_path": "planeta_kepler.png"
    },
    {
        "nome": "Mundo-Oceano de Gliese",
        "prod_base": 1200,
        "custo_base_upgrade": 20000,
        "imagem_path": "planeta_gliese.png"
    },
    {
        "nome": "Gigante Gasoso 'Nebula'",
        "prod_base": 5000,
        "custo_base_upgrade": 100000,
        "imagem_path": "planeta_nebula.png"
    },
    {
        "nome": "Planeta de Cristal 'Xylos'",
        "prod_base": 20000,
        "custo_base_upgrade": 500000,
        "imagem_path": "planeta_xylos.png"
    },
    {
        "nome": "Mundo-Colmeia 'Vespira'",
        "prod_base": 100000,
        "custo_base_upgrade": 2000000,
        "imagem_path": "planeta_vespira.png"
    },
    {
        "nome": "Forja Estelar 'Aethel'",
        "prod_base": 500000,
        "custo_base_upgrade": 10000000,
        "imagem_path": "planeta_aethel.png"
    },
    {
        "nome": "Centro Galático 'Nexus'",
        "prod_base": 2500000,
        "custo_base_upgrade": 50000000,
        "imagem_path": "planeta_nexus.png"
    }
]