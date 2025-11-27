import math
import pygame # Adicionamos o pygame aqui para carregar as imagens
from planetas import DADOS_TERRA_MAE, LISTA_PLANETAS_COLONIZAVEIS

class Planeta:
    """
    Representa um planeta individual que o jogador possui.
    Carrega a imagem específica dele.
    """
    def __init__(self, dados_estaticos):
        self.nome = dados_estaticos["nome"]
        self.prod_base = dados_estaticos["prod_base"]
        self.custo_base_upgrade = dados_estaticos["custo_base_upgrade"]
        self.imagem_path = dados_estaticos["imagem_path"]
        
        # Estado dinâmico (salvável)
        self.nivel = 1
        self.multiplicador_custo = 1.5 
        
        # Tenta carregar a imagem do disco
        self.sprite = self.carregar_sprite()

    def carregar_sprite(self):
        """Tenta carregar a imagem PNG. Se falhar, retorna None."""
        try:
            # Carrega a imagem
            img = pygame.image.load(self.imagem_path).convert_alpha()
            # Redimensiona para um tamanho padrão bonito (ex: 200x200 pixels)
            img = pygame.transform.scale(img, (200, 200))
            return img
        except Exception as e:
            print(f"Erro ao carregar imagem {self.imagem_path}: {e}")
            return None # Retorna None para usarmos um desenho padrão se a imagem falhar

    def get_producao_atual(self):
        return self.prod_base * self.nivel

    def get_custo_upgrade(self):
        return self.custo_base_upgrade * (self.multiplicador_custo ** (self.nivel - 1))

    def realizar_upgrade(self):
        self.nivel += 1

    def to_dict(self):
        return {
            "nome": self.nome,
            "nivel": self.nivel
        }

class Imperio:
    """
    Gerencia o estado global do jogador.
    """
    def __init__(self):
        self.pontos_galaticos = 0.0
        # Começa com a Terra-Mãe
        self.planetas_conquistados = [Planeta(DADOS_TERRA_MAE)]
        self.indice_proxima_colonizacao = 0 

    def get_producao_total_ps(self):
        total = 0
        for p in self.planetas_conquistados:
            total += p.get_producao_atual()
        return total

    def clicar_planeta(self, indice_planeta):
        if 0 <= indice_planeta < len(self.planetas_conquistados):
            planeta = self.planetas_conquistados[indice_planeta]
            ganho = max(1, planeta.get_producao_atual() * 0.1)
            self.pontos_galaticos += ganho
            return ganho
        return 0

    def tentar_upar_planeta(self, indice_planeta):
        if 0 <= indice_planeta < len(self.planetas_conquistados):
            planeta = self.planetas_conquistados[indice_planeta]
            custo = planeta.get_custo_upgrade()
            
            if self.pontos_galaticos >= custo:
                self.pontos_galaticos -= custo
                planeta.realizar_upgrade()
                return True
        return False

    def get_custo_proxima_colonizacao(self):
        if self.indice_proxima_colonizacao < len(LISTA_PLANETAS_COLONIZAVEIS):
            prox_dados = LISTA_PLANETAS_COLONIZAVEIS[self.indice_proxima_colonizacao]
            return prox_dados["custo_base_upgrade"] * 5 
        return None 

    def tentar_colonizar_novo(self):
        custo = self.get_custo_proxima_colonizacao()
        if custo is not None and self.pontos_galaticos >= custo:
            self.pontos_galaticos -= custo
            
            dados_novo = LISTA_PLANETAS_COLONIZAVEIS[self.indice_proxima_colonizacao]
            novo_planeta = Planeta(dados_novo)
            
            self.planetas_conquistados.append(novo_planeta)
            self.indice_proxima_colonizacao += 1
            return True
        return False