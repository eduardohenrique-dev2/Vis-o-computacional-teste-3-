import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

# ==========================
# CONFIGURAÇÃO DA INTERFACE
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema Inteligente de Monitoramento")
app.geometry("1200x760")

# ==========================
# CARREGA O YOLO
# ==========================

modelo = YOLO("yolov8n.pt")

# ==========================
# TÍTULO
# ==========================

titulo = ctk.CTkLabel(
    app,
    text="🎯 Sistema Inteligente de Monitoramento",
    font=("Arial", 30, "bold")
)

titulo.pack(pady=15)

# ==========================
# VÍDEO
# ==========================

video = ctk.CTkLabel(app, text="")
video.pack()

# ==========================
# PAINEL DE INFORMAÇÕES
# ==========================

# ==========================
# PAINEL DE INFORMAÇÕES
# ==========================

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

# ==========================
# CÂMERA
# ==========================

camera = cv2.VideoCapture(0)

# ==========================
# FUNÇÃO ATUALIZAR
# ==========================

def atualizar():

    ok, frame = camera.read()

    if ok:

        resultado = modelo(frame)

        frame_anotado = resultado[0].plot()

        pessoas = 0
        objetos = 0

        for deteccao in resultado[0].boxes:
            classe = int(deteccao.cls)
            nome_classe = modelo.names[classe]

            if nome_classe == "Pessoa":
                pessoas += 1
            else:
                objetos += 1

        lbl_pessoas.configure(text=str(pessoas))
        lbl_objetos.configure(text=str(objetos))

        frame_anotado = cv2.cvtColor(frame_anotado, cv2.COLOR_BGR2RGB)

        imagem = Image.fromarray(frame_anotado)
        imagem = imagem.resize((1100, 600))

        foto = ImageTk.PhotoImage(imagem)

        video.configure(image=foto)
        video.image = foto

        lbl_status.configure(text="🟢 Online", text_color="#00FF00")

    else:

        lbl_status.configure(text="🔴 Offline", text_color="#FF0000")

    app.after(10, atualizar)

# ==========================
# FECHAR
# ==========================

def fechar():

    camera.release()

    cv2.destroyAllWindows()

    app.destroy()

app.protocol("WM_DELETE_WINDOW", fechar)

# ==========================
# INICIA
# ==========================

atualizar()

app.mainloop()