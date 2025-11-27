import pygame
import random

# Inicializa as fontes aqui
pygame.font.init()

# --- Cores dos Efeitos ---
COLOR_PRODUCAO_EFEITO = (150, 255, 150) # Verde para produção
COLOR_CLIQUE_EFEITO = (255, 255, 150)   # Amarelo para cliques e avisos
COLOR_OUTLINE = (0, 0, 0)               # Contorno preto

# --- Fontes dos Efeitos ---
font_efeito = pygame.font.SysFont("Comic Sans MS", 24, bold=True)


class EfeitoFlutuante:
    """
    Controla um único texto flutuante (ex: '+10' ou 'LEVEL UP!')
    """
    def __init__(self, texto, x, y, cor, tempo_vida_ms=1000):
        self.x = x
        self.y = y
        self.cor = cor
        self.tempo_vida_total = tempo_vida_ms
        self.tempo_restante = tempo_vida_ms
        self.velocidade_y = -50 # Pixels por segundo (para cima)
        
        # Pré-renderiza o texto para performance
        self.texto_surf = font_efeito.render(texto, True, self.cor)
        self.outline_surf = font_efeito.render(texto, True, COLOR_OUTLINE)

    def update(self, dt):
        self.tempo_restante -= dt * 1000
        # Move para cima
        self.y += self.velocidade_y * dt
        return self.tempo_restante > 0

    def draw(self, screen):
        # Calcula transparência (fade out no final)
        alpha = 255
        if self.tempo_restante < 300: # Nos últimos 300ms, começa a sumir
            alpha = int((self.tempo_restante / 300) * 255)
            self.texto_surf.set_alpha(alpha)
            self.outline_surf.set_alpha(alpha)
        
        # Desenha contorno (offset simples)
        screen.blit(self.outline_surf, (self.x - 2, self.y))
        screen.blit(self.outline_surf, (self.x + 2, self.y))
        screen.blit(self.outline_surf, (self.x, self.y - 2))
        screen.blit(self.outline_surf, (self.x, self.y + 2))
        
        # Desenha texto principal
        screen.blit(self.texto_surf, (self.x, self.y))


class GerenciadorDeEfeitos:
    """
    Controla todos os efeitos flutuantes na tela.
    """
    def __init__(self):
        self.efeitos = []

    def spawn_production_effect(self, valor, x, y):
        """Cria um novo efeito de produção (verde)."""
        if valor < 1:
            return 
        
        texto = f"+{int(valor)}"
        # Adiciona variação aleatória na posição inicial
        x_final = x + random.randint(-20, 20)
        y_final = y + random.randint(-10, 10)
        
        novo_efeito = EfeitoFlutuante(texto, x_final, y_final, COLOR_PRODUCAO_EFEITO)
        self.efeitos.append(novo_efeito)

    def spawn_click_effect(self, valor_ou_texto, x, y):
        """
        Cria um novo efeito de clique (amarelo).
        Aceita tanto números (ex: 10) quanto texto (ex: "LEVEL UP!")
        """
        # --- CORREÇÃO DO ERRO AQUI ---
        # Verifica se é número (int ou float)
        if isinstance(valor_ou_texto, (int, float)):
            texto = f"+{int(valor_ou_texto)}"
        else:
            # Se for string, usa o texto direto
            texto = str(valor_ou_texto)

        novo_efeito = EfeitoFlutuante(texto, x, y, COLOR_CLIQUE_EFEITO, tempo_vida_ms=800)
        self.efeitos.append(novo_efeito)

    def update_e_desenha(self, screen, dt):
        """Atualiza e desenha todos os efeitos ativos."""
        # Mantém apenas os efeitos que ainda estão vivos (retornam True no update)
        self.efeitos = [e for e in self.efeitos if e.update(dt)]
        
        for e in self.efeitos:
            e.draw(screen)