

from typing import Any, Dict, List, TypedDict, Tuple, cast

EPIS_OBRIGATORIOS: Dict[str, List[str]] = cast(Dict[str, List[str]], __import__("tradutor").EPIS_OBRIGATORIOS)


class ObjectDetected(TypedDict):
    classe: str
    x1: int
    y1: int
    x2: int
    y2: int
    confianca: float


class AggregatedEPIInfo(TypedDict):
    detectado: bool
    confianca: float
    classe: str


class AnalysisResult(TypedDict):
    total_pessoas: int
    epis_disponiveis: Dict[str, bool]
    pessoas_conformes: int
    pessoas_nao_conformes: int
    status_geral: str
    detalhes: List[Dict[str, Any]]


class InspecaoEPIs:
    """
    Analisa detecções para verificar conformidade com EPIs.
    
    Fluxo:
    1. Recebe lista de objetos detectados
    2. Filtra apenas EPIs obrigatórios
    3. Agrupa EPIs por pessoa (proximidade espacial)
    4. Determina status de conformidade
    5. Retorna relatório detalhado
    """

    def __init__(self, modelo: Any) -> None:
        """
        Inicializa o inspector de EPIs.
        
        Args:
            modelo: Objeto YOLO com .names (dict de classes)
        """
        self.modelo: Any = modelo
        self.epis_disponiveis: Dict[str, bool] = self._detectar_epis_disponiveis()
        self.mapa_reverso: Dict[str, str] = {}
        self._criar_mapa_reverso()

    def _criar_mapa_reverso(self) -> None:
        """
        Cria um dicionário que mapeia nome traduzido -> nome original.
        
        Exemplo:
            "Capacete" -> "helmet"
            "Pessoa" -> "person"
        """
        from tradutor import CLASSES_PT
        
        self.mapa_reverso = {}
        
        for nome_original, nome_traduzido in CLASSES_PT.items():
            self.mapa_reverso[nome_traduzido] = nome_original

    def _detectar_epis_disponiveis(self) -> Dict[str, bool]:
        """
        Verifica quais EPIs o modelo consegue detectar.
        
        Retorna dict com estrutura:
        {
            "capacete": True,
            "colete": False,
            ...
        }
        """
        epis: Dict[str, bool] = {}
        nomes_modelo: List[str] = [nome.lower() for nome in self.modelo.names.values()]
        
        for categoria_epi, nomes_epi in EPIS_OBRIGATORIOS.items():
            # Verifica se algum nome de EPI dessa categoria existe no modelo
            detectavel = any(
                nome in nomes_modelo for nome in nomes_epi
            )
            epis[categoria_epi] = detectavel
        
        return epis

    def analisar(self, lista_objetos: List[Dict[str, Any]]) -> AnalysisResult:
        """
        Analisa objetos detectados para conformidade de EPIs.
        
        Args:
            lista_objetos: Lista com dicts contendo:
                - classe: str (nome traduzido)
                - x1, y1, x2, y2: coordenadas
                - confianca: float
        
        Retorna:
            dict com análise de EPIs
        """
        # Separa pessoas e EPIs
        pessoas: List[Dict[str, Any]] = []
        epis_detectados: List[Dict[str, Any]] = []
        
        for obj in lista_objetos:
            classe_original = self._obter_classe_original(obj['classe'])
            
            if classe_original == "person":
                pessoas.append(obj)
            elif self._eh_epi(classe_original):
                epis_detectados.append(obj)
        
        # Analisa conformidade
        resultado: AnalysisResult = {
            "total_pessoas": len(pessoas),
            "epis_disponiveis": self.epis_disponiveis,
            "pessoas_conformes": 0,
            "pessoas_nao_conformes": 0,
            "status_geral": "Conforme",
            "detalhes": []
        }
        
        # Para cada pessoa, verifica EPIs próximos
        for idx, pessoa in enumerate(pessoas):
            analise_pessoa = self._analisar_pessoa(
                pessoa,
                epis_detectados,
                idx
            )
            resultado["detalhes"].append(analise_pessoa)
            
            if analise_pessoa["conforme"]:
                resultado["pessoas_conformes"] += 1
            else:
                resultado["pessoas_nao_conformes"] += 1
                resultado["status_geral"] = "Nao Conforme"
        
        return resultado

    def _analisar_pessoa(self, pessoa: Dict[str, Any], epis_detectados: List[Dict[str, Any]], indice: int) -> Dict[str, Any]:
        """
        Analisa EPIs de uma pessoa específica.
        
        Args:
            pessoa: dict com coordenadas da pessoa
            epis_detectados: lista de EPIs próximos
            indice: índice da pessoa
        
        Retorna:
            dict com análise detalhada
        """
        # EPIs encontrados próximos a esta pessoa
        epis_proximos = self._encontrar_epis_proximos(
            pessoa,
            epis_detectados
        )
        
        # Agrupa EPIs por categoria
        epis_agrupados = self._agrupar_epis(epis_proximos)
        
        # Verifica conformidade
        conforme, faltantes = self._verificar_conformidade(
            epis_agrupados
        )
        
        return {
            "indice": indice + 1,
            "pessoa": pessoa,
            "epis_detectados": epis_agrupados,
            "epis_faltantes": faltantes,
            "conforme": conforme,
            "status": "Conforme" if conforme else "Nao Conforme"
        }

    def _encontrar_epis_proximos(self, pessoa: Dict[str, Any], epis_detectados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Encontra EPIs que estão próximos à pessoa (mesma região).
        
        Usa distância entre caixas como critério.
        """
        p_x1, p_y1, p_x2, p_y2 = (
            pessoa["x1"],
            pessoa["y1"],
            pessoa["x2"],
            pessoa["y2"]
        )
        
        # Centro e altura da pessoa
        p_centro_x = (p_x1 + p_x2) // 2
        p_altura = p_y2 - p_y1
        
        # Raio de proximidade (1.5x altura da pessoa)
        raio = int(p_altura * 1.5)
        
        epis_proximos: List[Dict[str, Any]] = []
        
        for epi in epis_detectados:
            e_x1, _e_y1, e_x2, _e_y2 = (
                epi["x1"],
                epi["y1"],
                epi["x2"],
                epi["y2"]
            )
            
            e_centro_x = (e_x1 + e_x2) // 2
            distancia = abs(p_centro_x - e_centro_x)
            
            # Se EPI está dentro do raio de proximidade
            if distancia < raio:
                epis_proximos.append(epi)
        
        return epis_proximos

    def _agrupar_epis(self, epis_proximidad: List[Dict[str, Any]]) -> Dict[str, AggregatedEPIInfo]:
        """
        Agrupa EPIs encontrados por categoria.
        
        Retorna dict como:
        {
            "capacete": {"detectado": True, "confianca": 0.95},
            "colete": {"detectado": False, "confianca": 0.0}
        }
        """
        agrupado: Dict[str, AggregatedEPIInfo] = {}
        
        # Inicializa com False
        for categoria in EPIS_OBRIGATORIOS.keys():
            agrupado[categoria] = {
                "detectado": False,
                "confianca": 0.0,
                "classe": ""
            }
        
        # Processa EPIs encontrados
        for epi in epis_proximidad:
            classe_original = self._obter_classe_original(epi['classe'])
            
            # Procura qual categoria este EPI pertence
            for categoria, nomes in EPIS_OBRIGATORIOS.items():
                if classe_original in nomes:
                    # Mantém o de maior confiança
                    if epi['confianca'] > agrupado[categoria]['confianca']:
                        agrupado[categoria] = {
                            "detectado": True,
                            "confianca": epi['confianca'],
                            "classe": epi['classe']
                        }
                    break
        
        return agrupado

    def _verificar_conformidade(self, epis_agrupados: Dict[str, AggregatedEPIInfo]) -> Tuple[bool, List[str]]:
        """
        Verifica se a pessoa está conforme com EPIs obrigatórios.
        
        Retorna:
            (conforme: bool, faltantes: list)
        """
        faltantes: List[str] = []
        
        for categoria, info in epis_agrupados.items():
            # Se o EPI não é detectável no modelo, ignora
            if not self.epis_disponiveis.get(categoria, False):
                continue

            # Se o EPI é detectável mas não foi encontrado
            if not info['detectado']:
                faltantes.append(categoria)
        
        conforme = len(faltantes) == 0
        
        return conforme, faltantes

    def _eh_epi(self, nome_classe: str) -> bool:
        """Verifica se uma classe é um EPI obrigatório."""
        for nomes_epi in EPIS_OBRIGATORIOS.values():
            if nome_classe in nomes_epi:
                return True
        return False

    def _obter_classe_original(self, classe_traduzida: str) -> str:
        """
        Retorna o nome original da classe a partir do traduzido.
        
        Usa mapa reverso criado em __init__.
        """
        # Tenta encontrar no mapa reverso
        if classe_traduzida in self.mapa_reverso:
            return self.mapa_reverso[classe_traduzida]
        
        # Fallback: tenta minúscula
        return classe_traduzida.lower()

    def gerar_texto_status(self, resultado: Dict[str, Any]) -> str:
        """
        Gera texto formatado do status geral.
        
        Retorna:
            str com status e quantidade de pessoas conformes
        """
        total = resultado["total_pessoas"]
        conformes = resultado["pessoas_conformes"]
        
        if total == 0:
            return "Nenhuma pessoa detectada"
        
        if conformes == total:
            return f"[OK] {conformes}/{total} Conforme"
        
        return f"[!] {conformes}/{total} Conforme"

    def gerar_relatorio_pessoa(self, detalhes_pessoa: Dict[str, Any]) -> str:
        """
        Gera relatório textual de uma pessoa específica.
        
        Retorna:
            str formatado com informações de EPIs
        """
        texto = f"Pessoa {detalhes_pessoa['indice']}: {detalhes_pessoa['status']}\n"
        
        epis = detalhes_pessoa['epis_detectados']
        
        # Lista EPIs encontrados
        encontrados: List[str] = []
        for info in epis.values():
            if info['detectado']:
                encontrados.append(f"  [+] {info['classe']}")
        
        if encontrados:
            texto += "Detectados:\n" + "\n".join(encontrados) + "\n"
        
        # Lista EPIs faltantes
        faltantes = detalhes_pessoa['epis_faltantes']
        if faltantes:
            texto += "Faltantes:\n"
            for faltante in faltantes:
                texto += f"  [-] {faltante.replace('_', ' ').title()}\n"
        
        return texto
