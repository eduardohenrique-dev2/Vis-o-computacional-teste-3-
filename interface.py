

import customtkinter as ctk
import tkinter as tk

from datetime import datetime
from PIL import Image, ImageTk
import cv2
import time

from config import *
from camera import Camera
from detector import Detector
from inspecao_epis import InspecaoEPIs

ctk.set_appearance_mode(TEMA)
ctk.set_default_color_theme(COR_TEMA)


class Interface:

    def __init__(self):

        # ==========================================
        # JANELA
        # ==========================================

        self.app = ctk.CTk()

        self.app.title(TITULO)

        self.app.geometry(
            f"{LARGURA_JANELA}x{ALTURA_JANELA}"
        )

        self.app.minsize(1200, 750)

        # ==========================================
        # GRID PRINCIPAL
        # ==========================================

        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(1, weight=1)

        # ==========================================
        # MENU LATERAL
        # ==========================================

        self.menu = ctk.CTkFrame(
            self.app,
            width=220,
            corner_radius=0
        )

        self.menu.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="ns"
        )

        # ------------------------------------------

        self.logo = ctk.CTkLabel(
            self.menu,
            text="🤖 VISÃO IA",
            font=(FONTE, 24, "bold")
        )

        self.logo.pack(pady=(30, 40))

        # ------------------------------------------

        botoes = [

            "🏠 Dashboard",

            "📷 Câmeras",

            "👤 Pessoas",

            "📦 Objetos",

            "📈 Estatísticas",

            "💾 Histórico",

            "⚙ Configurações"

        ]

        for texto in botoes:

            botao = ctk.CTkButton(

                self.menu,

                text=texto,

                width=180,

                height=40

            )

            botao.pack(pady=8)

        # ==========================================
        # CABEÇALHO
        # ==========================================

        self.topo = ctk.CTkFrame(
            self.app,
            height=70
        )

        self.topo.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.topo.grid_columnconfigure(1, weight=1)

        self.titulo = ctk.CTkLabel(

            self.topo,

            text="Sistema Inteligente de Visão Computacional",

            font=(FONTE, 28, "bold")

        )

        self.titulo.grid(
            row=0,
            column=0,
            padx=20
        )

        self.relogio = ctk.CTkLabel(

            self.topo,

            text="00:00:00",

            font=(FONTE, 22)

        )

        self.relogio.grid(
            row=0,
            column=2,
            padx=20
        )

        # ==========================================
        # CONTEÚDO
        # ==========================================

        self.conteudo = ctk.CTkFrame(
            self.app
        )

        self.conteudo.grid(

            row=1,

            column=1,

            sticky="nsew",

            padx=10,

            pady=(0,10)

        )

        self.conteudo.grid_columnconfigure(
            0,
            weight=3
        )

        self.conteudo.grid_columnconfigure(
            1,
            weight=1
        )

        # ==========================================
        # VIDEO
        # ==========================================

        self.frame_video = ctk.CTkFrame(
            self.conteudo
        )

        self.frame_video.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=10,

            pady=10

        )

        self.label_video = tk.Label(

            self.frame_video,

            bg="black"

        )

        self.label_video.pack(
            padx=10,
            pady=10
        )

        # ==========================================
        # PAINEL DIREITO
        # ==========================================

        self.painel = ctk.CTkFrame(
            self.conteudo,
            width=320
        )

        self.painel.grid(

            row=0,

            column=1,

            sticky="ns",

            padx=10,

            pady=10

        )

        # ==========================================
        # CARD PESSOAS
        # ==========================================

        self.card_pessoas = ctk.CTkFrame(
            self.painel
        )

        self.card_pessoas.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(

            self.card_pessoas,

            text="👤 Pessoas",

            font=(FONTE,18)

        ).pack(pady=(10,0))

        self.lbl_pessoas = ctk.CTkLabel(

            self.card_pessoas,

            text="0",

            font=(FONTE,38,"bold"),

            text_color=COR_VERDE

        )

        self.lbl_pessoas.pack(pady=(0,10))

        # ==========================================
        # CARD OBJETOS
        # ==========================================

        self.card_objetos = ctk.CTkFrame(
            self.painel
        )

        self.card_objetos.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(

            self.card_objetos,

            text="📦 Objetos",

            font=(FONTE,18)

        ).pack(pady=(10,0))

        self.lbl_objetos = ctk.CTkLabel(

            self.card_objetos,

            text="0",

            font=(FONTE,38,"bold"),

            text_color=COR_AZUL

        )

        self.lbl_objetos.pack(pady=(0,10))

        # ==========================================
        # CARD FPS
        # ==========================================

        self.card_fps = ctk.CTkFrame(
            self.painel
        )

        self.card_fps.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(

            self.card_fps,

            text="⚡ FPS",

            font=(FONTE,18)

        ).pack(pady=(10,0))

        self.lbl_fps = ctk.CTkLabel(

            self.card_fps,

            text="0",

            font=(FONTE,30,"bold")

        )

        self.lbl_fps.pack(pady=(0,10))

        # ==========================================
        # STATUS
        # ==========================================

        self.card_status = ctk.CTkFrame(
            self.painel
        )

        self.card_status.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(

            self.card_status,

            text="Status",

            font=(FONTE,18)

        ).pack(pady=(10,0))

        self.lbl_status = ctk.CTkLabel(

            self.card_status,

            text="🟢 Online",

            font=(FONTE,22,"bold"),

            text_color=COR_VERDE

        )

        self.lbl_status.pack(
            pady=(0,10)
        )

        # ==========================================
        # PAINEL INSPEÇÃO DE EPIs
        # ==========================================

        self.card_epis = ctk.CTkFrame(
            self.painel
        )

        self.card_epis.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(

            self.card_epis,

            text="Inspecao de EPIs",

            font=(FONTE, 18, "bold")

        ).pack(pady=(10, 5))

        self.lbl_status_epis = ctk.CTkLabel(

            self.card_epis,

            text="[OK] Conforme",

            font=(FONTE, 16, "bold"),

            text_color=COR_VERDE

        )

        self.lbl_status_epis.pack(pady=(0, 10))

        # Textbox com detalhes de EPIs
        self.lista_epis = ctk.CTkTextbox(

            self.card_epis,

            width=280,

            height=150,

            font=(FONTE, 12)

        )

        self.lista_epis.pack(
            padx=10,
            pady=10
        )

        self.lista_epis.insert(
            "0.0",
            "Nenhuma pessoa detectada..."
        )

        self.lista_epis.configure(
            state="disabled"
        )

        # ==========================================
        # OBJETOS DETECTADOS
        # ==========================================

        ctk.CTkLabel(

            self.painel,

            text="Objetos Detectados",

            font=(FONTE,20,"bold")

        ).pack(pady=(15,5))

        self.lista_objetos = ctk.CTkTextbox(

            self.painel,

            width=280,

            height=200

        )

        self.lista_objetos.pack(
            padx=15,
            pady=10
        )

        self.lista_objetos.insert(
            "0.0",
            "Nenhum objeto detectado..."
        )

        self.lista_objetos.configure(
            state="disabled"
        )

        # ==========================================
        # CÂMERA
        # ==========================================

        self.camera = Camera()

        # ==========================================
        # DETECTOR IA
        # ==========================================

        self.detector = Detector()

        # ==========================================
        # INSPEÇÃO DE EPIs
        # ==========================================

        self.inspecao_epis = InspecaoEPIs(
            self.detector.modelo
        )

        # ==========================================
        # FPS
        # ==========================================

        self.tempo_anterior = time.time()

        # ==========================================
        # INICIAR RELÓGIO
        # ==========================================

        self.atualizar_relogio()

        # ==========================================
        # INICIAR CÂMERA
        # ==========================================

        self.atualizar_camera()

        # ==========================================
        # FECHAR
        # ==========================================

        self.app.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )

# ==========================================================
# RELÓGIO
# ==========================================================

    def atualizar_relogio(self):

        agora = datetime.now()

        self.relogio.configure(
            text=agora.strftime("%d/%m/%Y  %H:%M:%S")
        )

        self.app.after(
            1000,
            self.atualizar_relogio
        )


# ==========================================================
# ATUALIZAR CÂMERA
# ==========================================================

    def atualizar_camera(self):

        ok, frame = self.camera.ler()

        if ok:

            resultado = self.detector.detectar(frame)

            frame = resultado["frame"]

            pessoas = resultado["pessoas"]

            objetos = resultado["objetos"]

            lista = resultado["lista"]

            # ---------------------------
            # Atualiza Cards
            # ---------------------------

            self.lbl_pessoas.configure(
                text=str(pessoas)
            )

            self.lbl_objetos.configure(
                text=str(objetos)
            )

            # ---------------------------
            # FPS
            # ---------------------------

            agora = time.time()

            fps = int(
                1 / (agora - self.tempo_anterior)
            )

            self.tempo_anterior = agora

            self.lbl_fps.configure(
                text=str(fps)
            )

            # ---------------------------
            # Lista Objetos
            # ---------------------------

            self.lista_objetos.configure(
                state="normal"
            )

            self.lista_objetos.delete(
                "1.0",
                "end"
            )

            if len(lista) == 0:

                self.lista_objetos.insert(
                    "end",
                    "Nenhum objeto detectado."
                )

            else:

                for objeto in lista:

                    texto = (
                        f"{objeto['classe']}   "
                        f"{objeto['confianca']*100:.1f}%\n"
                    )

                    self.lista_objetos.insert(
                        "end",
                        texto
                    )

            self.lista_objetos.configure(
                state="disabled"
            )

            # ---------------------------
            # Análise de EPIs
            # ---------------------------

            if INSPECAO_EPIS_ATIVA:

                resultado_epis = self.inspecao_epis.analisar(lista)

                self._atualizar_painel_epis(resultado_epis)

            # ---------------------------
            # OpenCV -> RGB
            # ---------------------------

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            imagem = Image.fromarray(frame)

            imagem = imagem.resize(
                (
                    LARGURA_VIDEO,
                    ALTURA_VIDEO
                )
            )

            foto = ImageTk.PhotoImage(imagem)

            self.label_video.configure(
                image=foto
            )

            self.label_video.image = foto

            self.lbl_status.configure(
                text="🟢 Online",
                text_color=COR_VERDE
            )

        else:

            self.lbl_status.configure(
                text="🔴 Offline",
                text_color=COR_VERMELHO
            )

        self.app.after(
            TEMPO_ATUALIZACAO,
            self.atualizar_camera
        )

# ==========================================================
# FECHAR SISTEMA
# ==========================================================

    def fechar(self):
        """
        Fecha a câmera e encerra o programa.
        """

        try:
            self.camera.fechar()
        except Exception:
            pass

        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

        self.app.destroy()


# ==========================================================
# ATUALIZAR STATUS
# ==========================================================

    def atualizar_status(self, texto, cor):

        self.lbl_status.configure(
            text=texto,
            text_color=cor
        )


# ==========================================================
# LIMPAR LISTA
# ==========================================================

    def limpar_lista(self):

        self.lista_objetos.configure(state="normal")

        self.lista_objetos.delete(
            "1.0",
            "end"
        )

        self.lista_objetos.insert(
            "end",
            "Nenhum objeto detectado..."
        )

        self.lista_objetos.configure(state="disabled")


# ==========================================================
# ADICIONAR OBJETO NA LISTA
# ==========================================================

    def adicionar_objeto(self, nome, confianca):

        self.lista_objetos.configure(state="normal")

        self.lista_objetos.insert(
            "end",
            f"{nome}   ({confianca:.1f}%)\n"
        )

        self.lista_objetos.see("end")

        self.lista_objetos.configure(state="disabled")


# ==========================================================
# ATUALIZAR PAINEL DE EPIs
# ==========================================================

    def _atualizar_painel_epis(self, resultado_epis):
        """
        Atualiza o painel de inspeção de EPIs com os resultados.

        Args:
            resultado_epis: dict retornado por InspecaoEPIs.analisar()
        """

        # Determina cor do status geral
        if resultado_epis["total_pessoas"] == 0:

            self.lista_epis.configure(state="normal")
            self.lista_epis.delete("1.0", "end")
            self.lista_epis.insert("0.0", "Nenhuma pessoa detectada...")
            self.lista_epis.configure(state="disabled")

            self.lbl_status_epis.configure(
                text="Sem detecções",
                text_color=COR_AZUL
            )

            return

        # Gera texto do status geral
        status_texto = self.inspecao_epis.gerar_texto_status(
            resultado_epis
        )

        # Cor baseada em conformidade
        if resultado_epis["pessoas_nao_conformes"] > 0:
            cor = COR_NAO_CONFORME
        else:
            cor = COR_CONFORME

        self.lbl_status_epis.configure(
            text=status_texto,
            text_color=cor
        )

        # Gera relatório detalhado
        texto_relatorio = ""

        for detalhes in resultado_epis["detalhes"]:

            texto_pessoa = self.inspecao_epis.gerar_relatorio_pessoa(
                detalhes
            )

            texto_relatorio += texto_pessoa + "\n"

        # Atualiza textbox
        self.lista_epis.configure(state="normal")
        self.lista_epis.delete("1.0", "end")
        self.lista_epis.insert("0.0", texto_relatorio)
        self.lista_epis.configure(state="disabled")


# ==========================================================
# EXECUTAR
# ==========================================================

    def executar(self):

        self.app.mainloop()