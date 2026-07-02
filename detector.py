
import cv2
from ultralytics import YOLO

from config import (
    MODELO_YOLO,
    CONFIANCA_MINIMA,
    ESPESSURA_CAIXA,
    ESPESSURA_TEXTO,
    ESCALA_TEXTO
)

from tradutor import traduzir


class Detector:

    def __init__(self):

        print("Carregando modelo YOLO...")

        self.modelo = YOLO(MODELO_YOLO)

        print("Modelo carregado com sucesso!")

    def detectar(self, frame):

        resultados = self.modelo(
            frame,
            conf=CONFIANCA_MINIMA,
            verbose=False
        )

        pessoas = 0
        objetos = 0

        lista_objetos = []

        for resultado in resultados:

            for box in resultado.boxes:

                classe = int(box.cls[0])

                nome_original = self.modelo.names[classe].lower()

                nome = traduzir(nome_original)

                confianca = float(box.conf[0])

                objetos += 1

                if nome_original == "person":
                    pessoas += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                lista_objetos.append({
                    "classe": nome,
                    "confianca": confianca,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                })

                # ===========================
                # Cor da caixa
                # ===========================

                if nome_original == "person":
                    cor = (0, 255, 0)

                elif nome_original in [
                    "cell phone",
                    "laptop",
                    "keyboard",
                    "mouse"
                ]:
                    cor = (255, 150, 0)

                elif nome_original in [
                    "bottle",
                    "cup"
                ]:
                    cor = (0, 255, 255)

                else:
                    cor = (255, 0, 255)

                # ===========================
                # Caixa
                # ===========================

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    cor,
                    ESPESSURA_CAIXA
                )

                texto = f"{nome} ({confianca*100:.0f}%)"

                largura = max(170, x2 - x1)

                cv2.rectangle(
                    frame,
                    (x1, y1 - 30),
                    (x1 + largura, y1),
                    cor,
                    -1
                )

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
            "lista": lista_objetos
        }