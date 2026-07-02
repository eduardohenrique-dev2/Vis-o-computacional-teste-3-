

import sqlite3
from datetime import datetime

from config import BANCO_DADOS


class Banco:

    def __init__(self):

        self.conexao = sqlite3.connect(
            BANCO_DADOS,
            check_same_thread=False
        )

        self.cursor = self.conexao.cursor()

        self.criar_tabelas()

    # =====================================================
    # CRIAR TABELAS
    # =====================================================

    def criar_tabelas(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS deteccoes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            data TEXT,

            hora TEXT,

            classe TEXT,

            confianca REAL,

            x1 INTEGER,

            y1 INTEGER,

            x2 INTEGER,

            y2 INTEGER

        )

        """)

        self.conexao.commit()

    # =====================================================
    # SALVAR DETECÇÃO
    # =====================================================

    def salvar(
        self,
        classe,
        confianca,
        x1,
        y1,
        x2,
        y2
    ):

        agora = datetime.now()

        data = agora.strftime("%d/%m/%Y")

        hora = agora.strftime("%H:%M:%S")

        self.cursor.execute("""

        INSERT INTO deteccoes(

            data,
            hora,
            classe,
            confianca,
            x1,
            y1,
            x2,
            y2

        )

        VALUES(?,?,?,?,?,?,?,?)

        """, (

            data,
            hora,
            classe,
            confianca,
            x1,
            y1,
            x2,
            y2

        ))

        self.conexao.commit()

    # =====================================================
    # TOTAL DE REGISTROS
    # =====================================================

    def total(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM deteccoes

        """)

        return self.cursor.fetchone()[0]

    # =====================================================
    # ÚLTIMAS DETECÇÕES
    # =====================================================

    def ultimas(self, limite=20):

        self.cursor.execute("""

        SELECT

            data,
            hora,
            classe,
            confianca

        FROM deteccoes

        ORDER BY id DESC

        LIMIT ?

        """, (limite,))

        return self.cursor.fetchall()

    # =====================================================
    # APAGAR BANCO
    # =====================================================

    def limpar(self):

        self.cursor.execute("""

        DELETE FROM deteccoes

        """)

        self.conexao.commit()

    # =====================================================
    # FECHAR
    # =====================================================

    def fechar(self):

        self.conexao.close()