
# ==========================================================
# JANELA
# ==========================================================

TITULO = "Sistema Inteligente de Visão Computacional"

LARGURA_JANELA = 1400
ALTURA_JANELA = 850

TELA_CHEIA = False


# ==========================================================
# TEMA
# ==========================================================

TEMA = "dark"              # dark | light

COR_TEMA = "blue"          # blue | green | dark-blue


# ==========================================================
# CÂMERA
# ==========================================================

ID_CAMERA = 0

LARGURA_CAMERA = 1280

ALTURA_CAMERA = 720

FPS_CAMERA = 30
FPS_DESEJADO = 30


# ==========================================================
# EXIBIÇÃO DO VÍDEO
# ==========================================================

LARGURA_VIDEO = 960

ALTURA_VIDEO = 540


# ==========================================================
# MODELO DE IA
# ==========================================================

# Modelo COCO padrão (80 classes)
MODELO_YOLO_COCO = "yolov8m.pt"

# Modelo com detecção de EPIs (PPE - Personal Protective Equipment)
MODELO_YOLO_PPE = "yolov8n.pt"

# Modelo ativo (altere para usar PPE em vez de COCO)
# Se o modelo PPE não existir, usar fallback para yolov8n disponível localmente
MODELO_YOLO = "yolov8n.pt"

CONFIANCA_MINIMA = 0.5


# ==========================================================
# INTERFACE
# ==========================================================

TEMPO_ATUALIZACAO = 10

MOSTRAR_FPS = True

MOSTRAR_CONFIANCA = True

MOSTRAR_STATUS = True

MOSTRAR_RELOGIO = True


# ==========================================================
# FONTES
# ==========================================================

FONTE = "Segoe UI"

FONTE_TITULO = 30

FONTE_SUBTITULO = 18

FONTE_CARD = 34

FONTE_NORMAL = 18

FONTE_PEQUENA = 14


# ==========================================================
# CORES
# ==========================================================

COR_VERDE = "#00C853"

COR_AZUL = "#2196F3"

COR_VERMELHO = "#F44336"

COR_AMARELO = "#FFC107"

COR_BRANCO = "#FFFFFF"

COR_PRETO = "#000000"

COR_CINZA = "#2B2B2B"

# ==========================================================
# DETECÇÃO
# ==========================================================

ESPESSURA_CAIXA = 2

ESPESSURA_TEXTO = 2

ESCALA_TEXTO = 0.65
# ==========================================================
# BANCO DE DADOS
# ==========================================================

BANCO_DADOS = "banco.db"


# ==========================================================
# RELATÓRIOS
# ==========================================================

PASTA_RELATORIOS = "relatorios"


# ==========================================================
# IMAGENS CAPTURADAS
# ==========================================================

PASTA_CAPTURAS = "capturas"


# ==========================================================
# LOGS
# ==========================================================

PASTA_LOGS = "logs"


# ==========================================================
# MODO DEBUG
# ==========================================================

DEBUG = False
# ==========================================================
# CORES DAS DETECÇÕES
# ==========================================================

COR_PESSOA = (0, 255, 0)

COR_GARRAFA = (0, 255, 255)

COR_ELETRONICO = (255, 180, 0)

COR_PADRAO = (255, 0, 255)
# ==========================================================
# SALVAR DETECÇÕES
# ==========================================================

SALVAR_IMAGENS = False

SALVAR_VIDEO = False

# ==========================================================
# INSPEÇÃO DE EPIs
# ==========================================================

INSPECAO_EPIS_ATIVA = True

COR_EPI_DETECTADO = "#00FF00"       # Verde

COR_EPI_NAO_DETECTADO = "#FF0000"   # Vermelho

COR_CONFORME = "#00C853"            # Verde escuro

COR_NAO_CONFORME = "#F44336"        # Vermelho