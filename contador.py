

import cv2


class Contador:

    def __init__(self):

        # Linha virtual
        self.posicao_linha = 300

        # Totais
        self.total_entradas = 0
        self.total_saidas = 0

        # Objetos já contabilizados
        self.ids_contados = set()

    # ==================================================

    def desenhar_linha(self, frame):

        altura, largura = frame.shape[:2]

        cv2.line(
            frame,
            (0, self.posicao_linha),
            (largura, self.posicao_linha),
            (0, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "LINHA DE CONTAGEM",
            (20, self.posicao_linha - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    # ==================================================

    def processar(self, frame, lista_objetos):

        """
        lista_objetos deve conter:

        x1
        y1
        x2
        y2
        classe
        """

        self.desenhar_linha(frame)

        for objeto in lista_objetos:

            if objeto["classe"] != "Pessoa":
                continue

            centro_x = int(
                (objeto["x1"] + objeto["x2"]) / 2
            )

            centro_y = int(
                (objeto["y1"] + objeto["y2"]) / 2
            )

            cv2.circle(
                frame,
                (centro_x, centro_y),
                5,
                (0, 0, 255),
                -1
            )

            objeto_id = f"{centro_x}_{centro_y}"

            if objeto_id in self.ids_contados:
                continue

            if centro_y > self.posicao_linha:

                self.total_entradas += 1

                self.ids_contados.add(objeto_id)

            elif centro_y < self.posicao_linha:

                self.total_saidas += 1

                self.ids_contados.add(objeto_id)

        return frame

    # ==================================================

    def entradas(self):

        return self.total_entradas

    # ==================================================

    def saidas(self):

        return self.total_saidas

    # ==================================================

    def dentro(self):

        return self.total_entradas - self.total_saidas

    # ==================================================

    def resetar(self):

        self.total_entradas = 0
        self.total_saidas = 0

        self.ids_contados.clear()