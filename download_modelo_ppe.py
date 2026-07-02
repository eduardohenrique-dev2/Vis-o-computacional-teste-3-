

import os
from pathlib import Path
from ultralytics import YOLO

# Modelo a usar (yolov8m tem mais capacidade de detecção)
MODELO_NOME = "yolov8m.pt"

# Caminho de destino
PASTA_MODELOS = "modelos"
ARQUIVO_MODELO = os.path.join(PASTA_MODELOS, "best-ppe.pt")

def criar_pasta_modelos():
    """Cria a pasta de modelos se não existir."""
    Path(PASTA_MODELOS).mkdir(exist_ok=True)
    print(f"[OK] Pasta '{PASTA_MODELOS}' criada/verificada")

def baixar_modelo():
    """Baixa e prepara o modelo YOLO."""
    
    print("\n" + "="*60)
    print("CARREGANDO/BAIXANDO MODELO YOLO")
    print("="*60)
    
    # Verifica se já existe
    if os.path.exists(ARQUIVO_MODELO):
        tamanho_mb = os.path.getsize(ARQUIVO_MODELO) / (1024 * 1024)
        print(f"\n[OK] Modelo já existe: {ARQUIVO_MODELO}")
        print(f"     Tamanho: {tamanho_mb:.1f} MB")
        return True
    
    print(f"\n[INFO] Carregando modelo YOLO: {MODELO_NOME}")
    print("[INFO] (Ultralytics baixará automaticamente se necessário)")
    
    try:
        # Carrega modelo (Ultralytics baixa automaticamente)
        print("[INFO] Aguarde, isso pode levar alguns minutos...")
        modelo = YOLO(MODELO_NOME)
        
        # Salva na pasta de modelos
        print(f"\n[INFO] Salvando modelo em: {ARQUIVO_MODELO}")
        modelo.save(ARQUIVO_MODELO)
        
        print("\n[OK] Modelo salvo com sucesso!")
        tamanho_mb = os.path.getsize(ARQUIVO_MODELO) / (1024 * 1024)
        print(f"[OK] Tamanho: {tamanho_mb:.1f} MB")
        
        return True
    
    except Exception as e:
        print(f"\n[ERRO] Falha ao carregar modelo: {e}")
        return False

def listar_classes_modelo():
    """Lista as classes detectadas pelo modelo."""
    try:
        print("\n[INFO] Carregando modelo para verificar classes...")
        modelo = YOLO(ARQUIVO_MODELO)
        
        print("\n[OK] Classes detectadas pelo modelo:")
        print("-" * 60)
        
        for idx, nome in modelo.names.items():
            print(f"  {idx:2d} - {nome}")
        
        print("-" * 40)
        
        # Verifica se tem EPIs
        epis = ["helmet", "hard hat", "safety vest", "mask", "gloves"]
        nomes_modelo = [n.lower() for n in modelo.names.values()]
        
        print("\n[OK] Verificação de EPIs:")
        for epi in epis:
            if any(epi in nm for nm in nomes_modelo):
                print(f"  [SIM] {epi}")
            else:
                print(f"  [NAO] {epi}")
        
    except Exception as e:
        print(f"\n[ERRO] Não foi possível carregar o modelo: {e}")

def main():
    """Função principal."""
    try:
        # Cria pasta
        criar_pasta_modelos()
        
        # Baixa modelo
        sucesso = baixar_modelo()
        
        if sucesso:
            # Lista classes
            listar_classes_modelo()
            
            print("\n" + "="*60)
            print("[OK] MODELO PRONTO PARA USO!")
            print("="*60)
            print("\nAgora execute: python main.py")
            print("\n")
            
            return 0
        else:
            print("\n[ERRO] Falha no download do modelo")
            return 1
    
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
