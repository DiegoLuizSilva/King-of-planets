import os
from colorama import init, Fore, Style

# Inicializa o Colorama
init(autoreset=True)

# ==========================================
# CORES PARA O TERMINAL (Colorama - Legacy)
# ==========================================
COR_PONTOS = Fore.BLUE + Style.BRIGHT  
COR_TITULO = Fore.CYAN + Style.BRIGHT
COR_PLANETA = Fore.WHITE + Style.BRIGHT
COR_SUCESSO = Fore.GREEN
COR_AVISO = Fore.YELLOW + Style.BRIGHT 
COR_ERRO = Fore.RED
COR_EVENTO = Fore.MAGENTA 

# ==========================================
# CORES PARA O PYGAME (RGB)
# ==========================================
# Interface / Fundo
COLOR_BG = (10, 10, 30)           # Fundo azul escuro espacial
COLOR_CARD = (30, 30, 50)         # Fundo de cartões/painéis
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Botões
COLOR_BUTTON = (50, 50, 80)
COLOR_BUTTON_DISABLED = (30, 30, 30)

# Elementos Específicos
COLOR_GREEN = (100, 255, 100)
COLOR_BLUE = (100, 150, 255)
COLOR_YELLOW = (255, 255, 100)
COLOR_RED = (255, 100, 100)
COLOR_PONTOS_RGB = (100, 200, 255) # Azul claro neon para os pontos

# Inputs de Texto
COLOR_INPUT_ACTIVE = (100, 100, 150)
COLOR_INPUT_INACTIVE = (50, 50, 70)

# ==========================================
# FUNÇÕES UTILITÁRIAS
# ==========================================

def limpar_tela():
    """Limpa o console para uma UI mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def formatar_numero_jogo(valor):
    """
    Formata números grandes para 1K, 1M, 1B, etc.
    Usa vírgula como separador decimal (PT-BR).
    """
    valor = float(valor)
    
    # Se for maior que 1 Quadrilhão
    if valor >= 1_000_000_000_000_000:
        texto = f"{valor/1_000_000_000_000_000:.2f}Q"
    # Se for maior que 1 Trilhão
    elif valor >= 1_000_000_000_000:
        texto = f"{valor/1_000_000_000_000:.2f}T"
    # Se for maior que 1 Bilhão
    elif valor >= 1_000_000_000:
        texto = f"{valor/1_000_000_000:.2f}B"
    # Se for maior que 1 Milhão
    elif valor >= 1_000_000:
        texto = f"{valor/1_000_000:.2f}M"
    # Se for maior que 1 Mil
    elif valor >= 1_000:
        texto = f"{valor/1_000:.2f}K"
    else:
        # Se for pequeno, apenas arredonda
        return str(int(valor))

    # Troca o ponto padrão do Python por vírgula e retorna
    return texto.replace(".", ",")