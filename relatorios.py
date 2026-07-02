
import os
import sqlite3
import pandas as pd

from datetime import datetime

from config import (
    BANCO_DADOS,
    PASTA_RELATORIOS
)


class Relatorios:

    def __init__(self):

        os.makedirs(PASTA_RELATORIOS, exist_ok=True)

        self.banco = BANCO_DADOS

    # =====================================================
    # LER BANCO
    # =====================================================

    def carregar_dados(self):

        conexao = sqlite3.connect(self.banco)

        df = pd.read_sql_query(

            "SELECT * FROM deteccoes",

            conexao

        )

        conexao.close()

        return df

    # =====================================================
    # EXPORTAR EXCEL
    # =====================================================

    def exportar_excel(self):

        df = self.carregar_dados()

        nome = datetime.now().strftime(

            "Relatorio_%d-%m-%Y_%H-%M-%S.xlsx"

        )

        caminho = os.path.join(

            PASTA_RELATORIOS,

            nome

        )

        df.to_excel(

            caminho,

            index=False

        )

        return caminho

    # =====================================================
    # EXPORTAR CSV
    # =====================================================

    def exportar_csv(self):

        df = self.carregar_dados()

        nome = datetime.now().strftime(

            "Relatorio_%d-%m-%Y_%H-%M-%S.csv"

        )

        caminho = os.path.join(

            PASTA_RELATORIOS,

            nome

        )

        df.to_csv(

            caminho,

            index=False,

            encoding="utf-8-sig"

        )

        return caminho

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def estatisticas(self):

        df = self.carregar_dados()

        if df.empty:

            return {

                "total": 0,

                "classes": {}

            }

        total = len(df)

        classes = (

            df["classe"]

            .value_counts()

            .to_dict()

        )

        return {

            "total": total,

            "classes": classes

        }

    # =====================================================
    # RESUMO
    # =====================================================

    def resumo(self):

        dados = self.estatisticas()

        print("\n========== RESUMO ==========")

        print(

            f"Total de registros: {dados['total']}"

        )

        print("\nObjetos detectados:\n")

        for nome, qtd in dados["classes"].items():

            print(

                f"{nome}: {qtd}"

            )

        print("============================\n")