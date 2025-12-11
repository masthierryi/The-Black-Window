import os
import time

# Pega o caminho absoluto da pasta atual onde o script está
pasta_atual = os.path.abspath(os.getcwd())

# -----------------------------------------------------------------
# AVISO DE SEGURANÇA E CONTAGEM REGRESSIVA
# -----------------------------------------------------------------
print("="*60)
print("  AVISO DE EXCLUSÃO PERMANENTE DE PASTAS VAZIAS")
print("="*60)
print(f"Iniciando varredura em: {pasta_atual}")
print("Este script irá APAGAR PERMANENTEMENTE qualquer subpasta que")
print("não contenha NENHUM arquivo ou NENHUMA outra pasta dentro dela.")
print("\nEle NÃO vai apagar a pasta principal onde o script está,")
print("mesmo que ela fique vazia.")
print("\nVOCÊ TEM 5 SEGUNDOS PARA CANCELAR (Pressione Ctrl+C)")
print("="*60)

try:
    # Contagem regressiva
    for i in range(5, 0, -1):
        print(f"Iniciando em {i}...", end="\r") # O '\r' faz a linha se reescrever
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nOPERAÇÃO CANCELADA PELO USUÁRIO. Nenhuma pasta foi tocada.")
    exit() # Sai do script

print("\n\nIniciando processo de limpeza (de baixo para cima)...\n")
# -----------------------------------------------------------------

pastas_deletadas = 0

# os.walk(..., topdown=False) é o segredo:
# Ele lista as subpastas mais profundas PRIMEIRO, e vai subindo.
for dirpath, dirnames, filenames in os.walk(pasta_atual, topdown=False):
    
    # Normaliza os caminhos para comparação segura
    caminho_atual_normalizado = os.path.normpath(dirpath)
    pasta_raiz_normalizada = os.path.normpath(pasta_atual)

    # Nunca tenta deletar a pasta principal onde o script começou
    if caminho_atual_normalizado == pasta_raiz_normalizada:
        continue

    # Verifica se a pasta está vazia (sem subpastas e sem arquivos)
    if not dirnames and not filenames:
        try:
            os.rmdir(dirpath)
            print(f"[DELETADA] Pasta vazia: {dirpath}")
            pastas_deletadas += 1
        except OSError as e:
            # O erro mais comum é "A pasta não está vazia"
            # (pode ter arquivos ocultos do sistema, como Thumbs.db no Windows)
            print(f"  [AVISO] Não foi possível deletar {dirpath}. Motivo: {e}")
        except Exception as e:
            print(f"  [ERRO INESPERADO] {dirpath}: {e}")

print("\n" + "="*60)
print("Limpeza de pastas vazias concluída.")
print(f"Total de pastas deletadas: {pastas_deletadas}")
print("="*60)