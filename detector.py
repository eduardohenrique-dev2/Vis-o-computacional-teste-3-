"""
==========================================================
DETECTOR.PY
==========================================================

Responsável pela Inteligência Artificial

- Carrega o modelo YOLO
- Detecta pessoas e objetos
- Traduz automaticamente para português
- Desenha caixas coloridas
- Retorna estatísticas

==========================================================
"""

import cv2
from typing import Any, Dict, List, TypedDict, cast
from ultralytics import YOLO

from config import (
    MODELO_YOLO,
    CONFIANCA_MINIMA,
    ESPESSURA_CAIXA,
    ESPESSURA_TEXTO,
    ESCALA_TEXTO
)

from tradutor import traduzir


class DeteccaoResult(TypedDict):
    frame: Any
    pessoas: int
    objetos: int
    lista: List[Dict[str, Any]]


class Detector:

    def __init__(self):

        print("=" * 60)
        print("CARREGANDO MODELO YOLO...")
        print("=" * 60)

        self.modelo = YOLO(MODELO_YOLO)

        print("MODELO CARREGADO COM SUCESSO!")
        print("=" * 60)

    # =====================================================

    def cor_classe(self, classe: str) -> tuple[int, int, int]:

        cores = {

            "person": (0, 255, 0),

            "cell phone": (255, 150, 0),
            "laptop": (255, 150, 0),
            "keyboard": (255, 150, 0),
            "mouse": (255, 150, 0),

            "bottle": (0, 255, 255),
            "cup": (0, 255, 255),

            "helmet": (255, 0, 0),
            "hardhat": (255, 0, 0),

            "vest": (0, 140, 255),
            "safety vest": (0, 140, 255),

            "mask": (255, 0, 255),
            "face mask": (255, 0, 255),

            "headset": (0, 200, 255),
            "earmuffs": (0, 200, 255),
            "ear protection": (0, 200, 255)

        }

        return cores.get(classe, (180, 0, 255))

    # =====================================================

    def detectar(self, frame: Any) -> DeteccaoResult:

        resultados = cast(List[Any], self.modelo(
            frame,
            conf=CONFIANCA_MINIMA,
            verbose=False
        ))

        pessoas = 0
        objetos = 0

        lista: List[Dict[str, Any]] = []

        for resultado in resultados:
            for box in resultado.boxes:

                classe = int(box.cls[0])

                nome_original = self.modelo.names[classe].lower()

                nome = traduzir(nome_original)

                confianca = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                objetos += 1

                if nome_original == "person":
                    pessoas += 1

                lista.append({
                    "classe": nome,
                    "classe_original": nome_original,
                    "confianca": confianca,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                })

                cor = self.cor_classe(nome_original)

                # Caixa
                cv2.rectangle(frame, (x1, y1), (x2, y2), cor, ESPESSURA_CAIXA)

                texto = f"{nome} ({confianca*100:.0f}%)"

                (largura, _), _ = cv2.getTextSize(
                    texto,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    ESCALA_TEXTO,
                    ESPESSURA_TEXTO
                )

                cv2.rectangle(frame, (x1, y1 - 32), (x1 + largura + 12, y1), cor, -1)

                cv2.putText(
                    frame,
                    texto,
                    (x1 + 6, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    ESCALA_TEXTO,
                    (255, 255, 255),
                    ESPESSURA_TEXTO,
                    cv2.LINE_AA
                )

        return {
            "frame": frame,
            "pessoas": pessoas,
            "objetos": objetos,
            "lista": lista
        }