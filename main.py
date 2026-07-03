import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from typing import Any

from detector import Detector

# =====================================================
# DETECTOR
# =====================================================

detector = Detector()

# =====================================================
# INTERFACE
# =====================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema Inteligente de Monitoramento")
app.geometry("1200x760")

# =====================================================
# TÍTULO
# =====================================================

titulo = ctk.CTkLabel(
    app,
    text="🎯 Sistema Inteligente de Monitoramento",
    font=("Arial", 30, "bold")
)

titulo.pack(pady=15)

# =====================================================
# VÍDEO
# =====================================================

video = ctk.CTkLabel(app, text="")
video.pack()

# =====================================================
# PAINEL DE INFORMAÇÕES
# =====================================================

painel = ctk.CTkFrame(app, fg_color="transparent")
painel.pack(fill="x", padx=20, pady=15)

# -------------------------
# CARD PESSOAS
# -------------------------

card_pessoas = ctk.CTkFrame(
    painel,
    width=250,
    height=100,
    corner_radius=15
)

card_pessoas.grid(row=0, column=0, padx=15)

titulo_pessoas = ctk.CTkLabel(
    card_pessoas,
    text="👤 Pessoas",
    font=("Arial",18)
)

titulo_pessoas.pack(pady=(10,0))

lbl_pessoas = ctk.CTkLabel(
    card_pessoas,
    text="0",
    font=("Arial",34,"bold"),
    text_color="#00FF88"
)

lbl_pessoas.pack()

# -------------------------
# CARD OBJETOS
# -------------------------

card_objetos = ctk.CTkFrame(
    painel,
    width=250,
    height=100,
    corner_radius=15
)

card_objetos.grid(row=0,column=1,padx=15)

titulo_objetos = ctk.CTkLabel(
    card_objetos,
    text="📦 Objetos",
    font=("Arial",18)
)

titulo_objetos.pack(pady=(10,0))

lbl_objetos = ctk.CTkLabel(
    card_objetos,
    text="0",
    font=("Arial",34,"bold"),
    text_color="#4DA6FF"
)

lbl_objetos.pack()

# -------------------------
# CARD STATUS
# -------------------------

card_status = ctk.CTkFrame(
    painel,
    width=250,
    height=100,
    corner_radius=15
)

card_status.grid(row=0,column=2,padx=15)

titulo_status = ctk.CTkLabel(
    card_status,
    text="Status",
    font=("Arial",18)
)

titulo_status.pack(pady=(10,0))

lbl_status = ctk.CTkLabel(
    card_status,
    text="🟢 Online",
    font=("Arial",24,"bold"),
    text_color="#00FF00"
)

lbl_status.pack()

# =====================================================
# CÂMERA (tenta múltiplas fontes: ids 0-3, depois arquivo local)
# =====================================================

def open_camera_fallback() -> tuple:
    # tenta IDs de 0 a 3
    for cam_id in range(4):
        cap = cv2.VideoCapture(cam_id)
        if cap.isOpened():
            return cap, True
        else:
            try:
                cap.release()
            except Exception:
                pass

    # tenta arquivo de vídeo local comum
    import os
    for candidate in ("video.mp4", "sample.mp4", "camera.mp4"):
        if os.path.exists(candidate):
            cap = cv2.VideoCapture(candidate)
            if cap.isOpened():
                return cap, True

    return None, False


camera, CAMERA_AVAILABLE = open_camera_fallback()
CAMERA_FAILURES = 0

# =====================================================
# ATUALIZAÇÃO
# =====================================================

def atualizar():
    global CAMERA_AVAILABLE
    global CAMERA_FAILURES

    if not CAMERA_AVAILABLE or camera is None:
        lbl_status.configure(text="🔴 Offline", text_color="#FF0000")
        app.after(1000, atualizar)
        return

    ok, frame = camera.read()

    global CAMERA_FAILURES
    if not ok or frame is None:
        CAMERA_FAILURES += 1
        if CAMERA_FAILURES >= 5:
            # desabilita câmera para evitar flood de warnings
            try:
                camera.release()
            except Exception:
                pass
            CAMERA_AVAILABLE = False
            lbl_status.configure(text="🔴 Offline", text_color="#FF0000")
            app.after(1000, atualizar)
            return
        lbl_status.configure(text="🔴 Offline", text_color="#FF0000")
        app.after(1000, atualizar)
        return

    CAMERA_FAILURES = 0

    resultado = detector.detectar(frame)

    frame: Any = resultado["frame"]

    pessoas = resultado["pessoas"]

    objetos = resultado["objetos"]

    lbl_pessoas.configure(text=str(pessoas))

    lbl_objetos.configure(text=str(objetos))

    lbl_status.configure(
        text="🟢 Online",
        text_color="#00FF00"
    )

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # type: ignore

    imagem = Image.fromarray(frame)  # type: ignore

    imagem = imagem.resize((1100,600))

    foto = ImageTk.PhotoImage(imagem)

    video.configure(image=foto)

    video.image = foto

    app.after(10, atualizar)

# =====================================================
# FECHAR
# =====================================================

def fechar():

    if camera is not None:
        try:
            camera.release()
        except Exception:
            pass

    cv2.destroyAllWindows()

    app.destroy()

app.protocol("WM_DELETE_WINDOW", fechar)

# =====================================================
# INICIAR
# =====================================================

atualizar()

app.mainloop()
