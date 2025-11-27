import pygame
import sys

# Módulos do Jogo
from modelos import Imperio
from visuals import GerenciadorDeEfeitos
from usuarios import registrar_usuario, login_usuario

# Importando TUDO de utils
from utils import (
    formatar_numero_jogo,
    COLOR_BG, COLOR_WHITE, COLOR_BUTTON, COLOR_BUTTON_DISABLED,
    COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_RED,
    COLOR_INPUT_ACTIVE, COLOR_INPUT_INACTIVE, COLOR_PONTOS_RGB
)

# --- Configurações Iniciais ---
pygame.init()
pygame.font.init()

# --- Constantes da Janela ---
LARGURA_TELA = 400
ALTURA_TELA = 600
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
clock = pygame.time.Clock()

# --- Fontes ---
font_titulo = pygame.font.SysFont("Arial", 32, bold=True)
font_padrao = pygame.font.SysFont("Arial", 20)
font_botao = pygame.font.SysFont("Arial", 18, bold=True)
font_botao_pequeno = pygame.font.SysFont("Arial", 14)
font_pontos = pygame.font.SysFont("Consolas", 28, bold=True)
font_input = pygame.font.SysFont("Consolas", 22)

# --- Função Auxiliar para Texto ---
def draw_text(text, font, color, x, y, anchor="topleft"):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if anchor == "center":
        rect.center = (x, y)
    elif anchor == "topleft":
        rect.topleft = (x, y)
    screen.blit(surface, rect)

# --- Tela de Autenticação (Login/Registro) ---
def run_auth_screen(estado_inicial="LOGIN"):
    username_text = ""
    password_text = ""
    active_input = None 
    mensagem_erro = ""
    mensagem_sucesso = ""
    
    input_user_rect = pygame.Rect(50, 200, 300, 40)
    input_pass_rect = pygame.Rect(50, 280, 300, 40)
    btn_action_rect = pygame.Rect(100, 350, 200, 50)
    btn_switch_rect = pygame.Rect(50, 420, 300, 30)

    while True:
        screen.fill(COLOR_BG)
        titulo = "LOGIN" if estado_inicial == "LOGIN" else "REGISTRO"
        draw_text(titulo, font_titulo, COLOR_WHITE, LARGURA_TELA // 2, 100, anchor="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_user_rect.collidepoint(event.pos): active_input = "username"
                elif input_pass_rect.collidepoint(event.pos): active_input = "password"
                else: active_input = None
                
                if btn_action_rect.collidepoint(event.pos):
                    if estado_inicial == "LOGIN":
                        sucesso, msg = login_usuario(username_text, password_text)
                        if sucesso: return username_text 
                        else: mensagem_erro = msg
                    else: 
                        sucesso, msg = registrar_usuario(username_text, password_text)
                        if sucesso:
                            mensagem_sucesso = msg; mensagem_erro = ""; estado_inicial = "LOGIN" 
                        else: mensagem_erro = msg

                if btn_switch_rect.collidepoint(event.pos):
                    estado_inicial = "REGISTRO" if estado_inicial == "LOGIN" else "LOGIN"
                    mensagem_erro = ""; mensagem_sucesso = ""

            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE: username_text = username_text[:-1]
                    else: username_text += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE: password_text = password_text[:-1]
                    else: password_text += event.unicode

        color_input_user = COLOR_INPUT_ACTIVE if active_input == "username" else COLOR_INPUT_INACTIVE
        color_input_pass = COLOR_INPUT_ACTIVE if active_input == "password" else COLOR_INPUT_INACTIVE

        draw_text("Usuário:", font_botao, COLOR_WHITE, 50, 180)
        draw_text("Senha:", font_botao, COLOR_WHITE, 50, 260)

        mostrar_cursor = (pygame.time.get_ticks() // 500) % 2 == 0

        pygame.draw.rect(screen, color_input_user, input_user_rect, border_radius=5)
        txt_usr = username_text + ("|" if active_input == "username" and mostrar_cursor else "")
        screen.blit(font_input.render(txt_usr, True, COLOR_WHITE), (input_user_rect.x + 10, input_user_rect.y + 10))

        pygame.draw.rect(screen, color_input_pass, input_pass_rect, border_radius=5)
        txt_pass = ("*" * len(password_text)) + ("|" if active_input == "password" and mostrar_cursor else "")
        screen.blit(font_input.render(txt_pass, True, COLOR_WHITE), (input_pass_rect.x + 10, input_pass_rect.y + 10))

        pygame.draw.rect(screen, COLOR_BUTTON, btn_action_rect, border_radius=10)
        draw_text("ENTRAR" if estado_inicial == "LOGIN" else "CRIAR CONTA", font_botao, COLOR_WHITE, btn_action_rect.centerx, btn_action_rect.centery, anchor="center")
        draw_text("Não tem conta? Registre-se" if estado_inicial == "LOGIN" else "Já tem conta? Faça Login", font_botao_pequeno, COLOR_BLUE, btn_switch_rect.centerx, btn_switch_rect.centery, anchor="center")

        if mensagem_erro: draw_text(mensagem_erro, font_botao_pequeno, COLOR_RED, LARGURA_TELA//2, 460, anchor="center")
        if mensagem_sucesso: draw_text(mensagem_sucesso, font_botao_pequeno, COLOR_GREEN, LARGURA_TELA//2, 460, anchor="center")

        pygame.display.flip()
        clock.tick(30)


# --- Tela do Jogo Principal ---
def run_game(usuario):
    imperio = Imperio()
    efeitos = GerenciadorDeEfeitos()
    running = True
    
    # Índice do planeta que está sendo exibido na tela no momento
    indice_visualizacao = 0 
    
    # Áreas clicáveis
    area_planeta_rect = pygame.Rect(0, 120, LARGURA_TELA, 280)
    btn_upgrade_rect = pygame.Rect(50, 480, 300, 60)
    
    # Botões de Navegação (Setas)
    btn_esq_rect = pygame.Rect(10, 250, 40, 40)
    btn_dir_rect = pygame.Rect(LARGURA_TELA - 50, 250, 40, 40)

    while running:
        dt = clock.get_time() / 1000 
        
        # Produção Automática (soma de todos os planetas)
        producao_frame = imperio.get_producao_total_ps() * dt
        if producao_frame > 0:
            imperio.pontos_galaticos += producao_frame
        
        # --- Eventos ---
        click_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                
                # 1. Clique no Planeta (Farmar)
                if area_planeta_rect.collidepoint(click_pos):
                    # Só clica se estiver vendo um planeta conquistado
                    if indice_visualizacao < len(imperio.planetas_conquistados):
                        ganho = imperio.clicar_planeta(indice_visualizacao)
                        efeitos.spawn_click_effect(ganho, click_pos[0], click_pos[1])

                # 2. Navegação (Esquerda)
                if btn_esq_rect.collidepoint(click_pos):
                    if indice_visualizacao > 0:
                        indice_visualizacao -= 1

                # 3. Navegação (Direita)
                if btn_dir_rect.collidepoint(click_pos):
                    # Pode ir até len(planetas) se houver próxima colonização disponível
                    max_idx = len(imperio.planetas_conquistados)
                    if imperio.get_custo_proxima_colonizacao() is not None:
                         # Permite ir um slot a mais (o slot de "Comprar Novo")
                         if indice_visualizacao < max_idx:
                             indice_visualizacao += 1
                    else:
                        # Se já comprou tudo, limita ao ultimo planeta
                         if indice_visualizacao < max_idx - 1:
                             indice_visualizacao += 1

                # 4. Botão Principal (Upgrade ou Colonizar)
                if btn_upgrade_rect.collidepoint(click_pos):
                    # Se estiver vendo um planeta conquistado -> UPGRADE
                    if indice_visualizacao < len(imperio.planetas_conquistados):
                        if imperio.tentar_upar_planeta(indice_visualizacao):
                            efeitos.spawn_click_effect("LEVEL UP!", btn_upgrade_rect.centerx, btn_upgrade_rect.y)
                    
                    # Se estiver no slot vazio -> COLONIZAR
                    elif indice_visualizacao == len(imperio.planetas_conquistados):
                        if imperio.tentar_colonizar_novo():
                            efeitos.spawn_click_effect("NOVA COLÔNIA!", btn_upgrade_rect.centerx, btn_upgrade_rect.y)


        # --- Desenho ---
        screen.fill(COLOR_BG)
        
        # Topo
        draw_text(f"Império de {usuario}", font_padrao, COLOR_WHITE, 10, 10)
        texto_pontos = f"Pontos: {formatar_numero_jogo(imperio.pontos_galaticos)}"
        draw_text(texto_pontos, font_pontos, COLOR_PONTOS_RGB, LARGURA_TELA // 2, 50, anchor="center")
        
        # Info da Produção Total
        prod_total = formatar_numero_jogo(imperio.get_producao_total_ps())
        draw_text(f"Produção Total: {prod_total}/s", font_botao_pequeno, COLOR_GREEN, LARGURA_TELA // 2, 80, anchor="center")

        # --- Área Central (Carrossel) ---
        
        # Determina o que mostrar (Planeta ou Slot de Compra)
        vendo_planeta_existente = indice_visualizacao < len(imperio.planetas_conquistados)
        
        if vendo_planeta_existente:
            planeta_atual = imperio.planetas_conquistados[indice_visualizacao]
            
            # Título do Planeta e Nível
            draw_text(f"{planeta_atual.nome}", font_titulo, COLOR_WHITE, LARGURA_TELA//2, 130, anchor="center")
            draw_text(f"Nível {planeta_atual.nivel}", font_padrao, COLOR_BLUE, LARGURA_TELA//2, 165, anchor="center")
            
            # --- DESENHO DO PLANETA (IMAGEM OU CÍRCULO) ---
            if planeta_atual.sprite:
                # Se tem imagem carregada, usa ela
                rect_img = planeta_atual.sprite.get_rect()
                rect_img.center = area_planeta_rect.center
                screen.blit(planeta_atual.sprite, rect_img)
            else:
                # Fallback: Círculo Azul
                pygame.draw.circle(screen, (50, 100, 200), area_planeta_rect.center, 90)
                draw_text("🌍", pygame.font.SysFont("Segoe UI Emoji", 100), COLOR_WHITE, area_planeta_rect.centerx, area_planeta_rect.centery, anchor="center")
            
            # Info de Produção Individual
            prod_ind = formatar_numero_jogo(planeta_atual.get_producao_atual())
            draw_text(f"+{prod_ind}/s", font_botao, COLOR_GREEN, LARGURA_TELA//2, 380, anchor="center")

            # Botão de Upgrade
            custo_up = planeta_atual.get_custo_upgrade()
            pode_pagar = imperio.pontos_galaticos >= custo_up
            cor_btn = COLOR_BUTTON if pode_pagar else COLOR_BUTTON_DISABLED
            
            pygame.draw.rect(screen, cor_btn, btn_upgrade_rect, border_radius=10)
            draw_text("UPGRADE PLANETA", font_botao, COLOR_WHITE, btn_upgrade_rect.centerx, btn_upgrade_rect.centery - 10, anchor="center")
            draw_text(f"Custo: {formatar_numero_jogo(custo_up)}", font_botao_pequeno, COLOR_YELLOW, btn_upgrade_rect.centerx, btn_upgrade_rect.centery + 15, anchor="center")

        else:
            # Slot de Colonização (Comprar Novo)
            custo_colonia = imperio.get_custo_proxima_colonizacao()
            
            draw_text("Espaço Não Explorado", font_titulo, COLOR_WHITE, LARGURA_TELA//2, 130, anchor="center")
            
            # Círculo Cinza (Vazio)
            pygame.draw.circle(screen, (50, 50, 50), area_planeta_rect.center, 70, width=5)
            draw_text("?", font_titulo, (100,100,100), area_planeta_rect.centerx, area_planeta_rect.centery, anchor="center")

            if custo_colonia is not None:
                pode_pagar = imperio.pontos_galaticos >= custo_colonia
                cor_btn = COLOR_BUTTON if pode_pagar else COLOR_BUTTON_DISABLED
                
                pygame.draw.rect(screen, cor_btn, btn_upgrade_rect, border_radius=10)
                draw_text("COLONIZAR NOVO", font_botao, COLOR_WHITE, btn_upgrade_rect.centerx, btn_upgrade_rect.centery - 10, anchor="center")
                draw_text(f"Custo: {formatar_numero_jogo(custo_colonia)}", font_botao_pequeno, COLOR_YELLOW, btn_upgrade_rect.centerx, btn_upgrade_rect.centery + 15, anchor="center")
            else:
                draw_text("UNIVERSO DOMINADO!", font_titulo, COLOR_GREEN, LARGURA_TELA//2, 400, anchor="center")

        # --- Setas de Navegação ---
        # Seta Esquerda (se não for o primeiro)
        if indice_visualizacao > 0:
            pygame.draw.rect(screen, COLOR_BUTTON, btn_esq_rect, border_radius=5)
            draw_text("<", font_titulo, COLOR_WHITE, btn_esq_rect.centerx, btn_esq_rect.centery, anchor="center")
        
        # Seta Direita (se houver próximo planeta ou slot de colonização)
        max_idx = len(imperio.planetas_conquistados)
        if (indice_visualizacao < max_idx and imperio.get_custo_proxima_colonizacao() is not None) or (indice_visualizacao < max_idx - 1):
             pygame.draw.rect(screen, COLOR_BUTTON, btn_dir_rect, border_radius=5)
             draw_text(">", font_titulo, COLOR_WHITE, btn_dir_rect.centerx, btn_dir_rect.centery, anchor="center")

        # Efeitos Visuais
        efeitos.update_e_desenha(screen, dt)
        
        pygame.display.flip()
        clock.tick(60)
    
    return

def main():
    usuario_logado = None
    while True: 
        if not usuario_logado:
            pygame.display.set_caption("King of Planets 👑 - Login")
            usuario_logado = run_auth_screen(estado_inicial="LOGIN")
        if usuario_logado:
            pygame.display.set_caption(f"King of Planets 👑 - {usuario_logado}")
            run_game(usuario_logado)
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("\nERRO FATAL:"); traceback.print_exc(); input("Enter para fechar...")