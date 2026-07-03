"""
==========================================================
TRADUTOR.PY

Traduz automaticamente as classes do YOLO para português.

==========================================================
"""

CLASSES_PT = {

    # Pessoas
    "person": "Pessoa",

    # Veículos
    "bicycle": "Bicicleta",
    "car": "Carro",
    "motorcycle": "Motocicleta",
    "airplane": "Avião",
    "bus": "Ônibus",
    "train": "Trem",
    "truck": "Caminhão",
    "boat": "Barco",

    # Trânsito
    "traffic light": "Semáforo",
    "fire hydrant": "Hidrante",
    "stop sign": "Placa de Pare",
    "parking meter": "Parquímetro",

    # Objetos urbanos
    "bench": "Banco",

    # Animais
    "bird": "Pássaro",
    "cat": "Gato",
    "dog": "Cachorro",
    "horse": "Cavalo",
    "sheep": "Ovelha",
    "cow": "Vaca",
    "elephant": "Elefante",
    "bear": "Urso",
    "zebra": "Zebra",
    "giraffe": "Girafa",

    # Acessórios
    "backpack": "Mochila",
    "umbrella": "Guarda-chuva",
    "handbag": "Bolsa",
    "tie": "Gravata",
    "suitcase": "Mala",

    # Esportes
    "frisbee": "Frisbee",
    "skis": "Esquis",
    "snowboard": "Snowboard",
    "sports ball": "Bola",
    "kite": "Pipa",
    "baseball bat": "Taco",
    "baseball glove": "Luva de Beisebol",
    "skateboard": "Skate",
    "surfboard": "Prancha",
    "tennis racket": "Raquete",

    # Cozinha
    "bottle": "Garrafa",
    "wine glass": "Taça",
    "cup": "Copo",
    "fork": "Garfo",
    "knife": "Faca",
    "spoon": "Colher",
    "bowl": "Tigela",

    # Alimentos
    "banana": "Banana",
    "apple": "Maçã",
    "sandwich": "Sanduíche",
    "orange": "Laranja",
    "broccoli": "Brócolis",
    "carrot": "Cenoura",
    "hot dog": "Cachorro-quente",
    "pizza": "Pizza",
    "donut": "Rosquinha",
    "cake": "Bolo",

    # Móveis
    "chair": "Cadeira",
    "couch": "Sofá",
    "potted plant": "Planta",
    "bed": "Cama",
    "dining table": "Mesa",
    "toilet": "Vaso Sanitário",

    # Eletrônicos
    "tv": "Televisão",
    "laptop": "Notebook",
    "mouse": "Mouse",
    "remote": "Controle Remoto",
    "keyboard": "Teclado",
    "cell phone": "Celular",
    "microwave": "Micro-ondas",
    "oven": "Forno",
    "toaster": "Torradeira",
    "sink": "Pia",
    "refrigerator": "Geladeira",

    # Diversos
    "book": "Livro",
    "clock": "Relógio",
    "vase": "Vaso",
    "scissors": "Tesoura",
    "teddy bear": "Urso de Pelúcia",
    "hair drier": "Secador",
    "toothbrush": "Escova de Dentes",

    # ===========================
    # EPIs
    # ===========================

    "helmet": "Capacete",
    "hardhat": "Capacete",
    "vest": "Colete",
    "safety vest": "Colete de Segurança",
    "mask": "Máscara",
    "face mask": "Máscara Facial",
    "gloves": "Luvas",
    "goggles": "Óculos de Proteção",
    "glasses": "Óculos",
    "earmuffs": "Protetor Auricular",
    "headset": "Headset",
    "ear protection": "Protetor Auricular",
    "boots": "Botas",
    "safety shoes": "Botas de Segurança"
}


EPIS_OBRIGATORIOS = {
    "capacete": ["helmet", "hardhat"],
    "colete": ["vest", "safety vest"],
    "mascara": ["mask", "face mask"],
    "luvas": ["gloves"],
    "oculos": ["goggles", "glasses"],
    "protetor_auricular": ["earmuffs", "headset", "ear protection"],
    "botas": ["boots", "safety shoes"]
}


def traduzir(nome_classe: str) -> str:
    """
    Traduz o nome retornado pelo YOLO.
    """

    nome_classe = nome_classe.lower().strip()

    return CLASSES_PT.get(nome_classe, nome_classe)