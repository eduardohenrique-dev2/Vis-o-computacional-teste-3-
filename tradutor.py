"""
==========================================================
TRADUTOR DE CLASSES YOLO (COCO) PARA PORTUGUÊS
==========================================================

Responsável por traduzir automaticamente os nomes das
classes detectadas pelo YOLO.

Exemplo:

person  -> Pessoa
bottle  -> Garrafa
car     -> Carro

==========================================================
"""

CLASSES_PT = {

    "pessoa": "Pessoa",
    "bicicleta": "Bicicleta",
    "carro": "Carro",
    "motocicleta": "Motocicleta",
    "avião": "Avião",
    "ônibus": "Ônibus",
    "trem": "Trem",
    "caminhão": "Caminhão",
    "barco": "Barco",
    "semáforo": "Semáforo",
    "hidrante": "Hidrante",
    "placa de pare": "Placa de Pare",
    "parquímetro": "Parquímetro",
    "banco": "Banco",
    "pássaro": "Pássaro",
    "gato": "Gato",
    "cachorro": "Cachorro",
    "cavalo": "Cavalo",
    "ovelha": "Ovelha",
    "vaca": "Vaca",
    "elefante": "Elefante",
    "urso": "Urso",
    "zebra": "Zebra",
    "girafa": "Girafa",
    "mochila": "Mochila",
    "guarda-chuva": "Guarda-chuva",
    "bolsa": "Bolsa",
    "gravata": "Gravata",
    "mala": "Mala",
    "frisbee": "Frisbee",
    "esquis": "Esquis",
    "snowboard": "Snowboard",
    "sports ball": "Bola",
    "kite": "Pipa",
    "baseball bat": "Taco",
    "baseball glove": "Luva",
    "skateboard": "Skate",
    "surfboard": "Prancha",
    "tennis racket": "Raquete",
    "bottle": "Garrafa",
    "wine glass": "Taça",
    "cup": "Copo",
    "fork": "Garfo",
    "knife": "Faca",
    "spoon": "Colher",
    "bowl": "Tigela",
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
    "chair": "Cadeira",
    "couch": "Sofá",
    "potted plant": "Planta",
    "bed": "Cama",
    "dining table": "Mesa",
    "toilet": "Vaso Sanitário",
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
    "book": "Livro",
    "clock": "Relógio",
    "vase": "Vaso",
    "scissors": "Tesoura",
    "teddy bear": "Urso de Pelúcia",
    "hair drier": "Secador",
    "toothbrush": "Escova de Dentes",
    
    # ==============================================
    # EQUIPAMENTOS DE PROTEÇÃO INDIVIDUAL (EPIs)
    # ==============================================
    
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

# ==============================================
# EPIs OBRIGATÓRIOS (para análise)
# ==============================================

EPIS_OBRIGATORIOS = {
    "capacete": ["helmet", "hardhat"],
    "colete": ["vest", "safety vest"],
    "mascara": ["mask", "face mask"],
    "luvas": ["gloves"],
    "oculos": ["goggles", "glasses"],
    "protetor_auricular": ["earmuffs", "ear protection", "headset"],
    "botas": ["boots", "safety shoes"]
}


def traduzir(nome_classe: str) -> str:
    """
    Traduz o nome da classe para português.

    Caso a classe não exista no dicionário,
    retorna o próprio nome recebido.
    """

    return CLASSES_PT.get(nome_classe, nome_classe)