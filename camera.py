

import cv2

from config import (
    ID_CAMERA,
    LARGURA_CAMERA,
    ALTURA_CAMERA,
    FPS_CAMERA
)


class Camera:

    def __init__(self):

        self.camera = None

        self.abrir()


    # =====================================================
    # ABRIR CÂMERA
    # =====================================================

    def abrir(self):

        self.camera = cv2.VideoCapture(ID_CAMERA)

        if not self.camera.isOpened():

            raise Exception(
                "Não foi possível abrir a câmera."
            )

        # Resolução

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            LARGURA_CAMERA
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            ALTURA_CAMERA
        )

        # FPS

        self.camera.set(
            cv2.CAP_PROP_FPS,
            FPS_CAMERA
        )


    # =====================================================
    # LER FRAME
    # =====================================================

    def ler(self):

        if self.camera is None:

            return False, None

        sucesso, frame = self.camera.read()

        return sucesso, frame


    # =====================================================
    # RESOLUÇÃO ATUAL
    # =====================================================

    def resolucao(self):

        largura = int(
            self.camera.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        altura = int(
            self.camera.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        return largura, altura


    # =====================================================
    # FPS DA CÂMERA
    # =====================================================

    def fps(self):

        return int(
            self.camera.get(
                cv2.CAP_PROP_FPS
            )
        )


    # =====================================================
    # STATUS
    # =====================================================

    def online(self):

        if self.camera is None:

            return False

        return self.camera.isOpened()


    # =====================================================
    # FECHAR
    # =====================================================

    def fechar(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None