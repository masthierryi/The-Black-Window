import os
import time

# Pega o caminho absoluto da pasta onde o script está
pasta_atual = os.getcwd()

# Pega o caminho absoluto deste script para não se auto-deletar
try:
    # __file__ é o caminho do script sendo executado
    script_path = os.path.abspath(__file__)
except NameError:
    # Se estiver rodando de forma interativa
    script_path = os.path.join(pasta_atual, "limpar_tudo.py") # ATUALIZE SE O NOME FOR DIFERENTE
    
# -----------------------------------------------------------------
# AVISO DE SEGURANÇA E CONTAGEM REGRESSIVA
# -----------------------------------------------------------------
print("="*60)
print("  AVISO DE EXCLUSÃO PERMANENTE (INCLUINDO SUBPASTAS)")
print("="*60)
print("Este script irá APAGAR arquivos nesta pasta E EM TODAS AS SUBPASTAS se:")
print("  1. A extensão NÃO for '.mp3'")
print("  2. OU o nome contiver a palavra 'instrumental' (em maiúsculo ou minúsculo)")
print(f"\nO script em '{script_path}' será ignorado.")
print("\nVOCÊ TEM 5 SEGUNDOS PARA CANCELAR (Pressione Ctrl+C)")
print("="*60)

try:
    for i in range(5, 0, -1):
        print(f"Iniciando em {i}...", end="\r")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nOPERAÇÃO CANCELADA PELO USUÁRIO. Nenhum arquivo foi tocado.")
    exit()

print("\n\nIniciando processo de limpeza (incluindo subpastas)...\n")
# -----------------------------------------------------------------

arquivos_deletados = 0
arquivos_mantidos = 0

# os.walk() percorre a pasta atual (dirpath) E todas as suas subpastas
for dirpath, dirnames, filenames in os.walk(pasta_atual):
    print(f"--- Verificando Pasta: {dirpath} ---")
    
    for nome_do_arquivo in filenames:
        caminho_completo = os.path.join(dirpath, nome_do_arquivo)
        
        # Pula se for o próprio script
        # Compara caminhos absolutos para ter certeza
        if os.path.abspath(caminho_completo) == script_path:
            print(f"  [IGNORADO] (Este é o script de limpeza)")
            continue

        nome_lower = nome_do_arquivo.lower()
        
        # --- A LÓGICA DE EXCLUSÃO ---
        nao_e_mp3 = not nome_lower.endswith('.mp3')
        e_instrumental = 'instrumental' in nome_lower
        
        if nao_e_mp3 or e_instrumental:
            try:
                os.remove(caminho_completo)
                print(f"  [DELETADO] {nome_do_arquivo}")
                arquivos_deletados += 1
            except Exception as e:
                print(f"  [ERRO] Não foi possível deletar {nome_do_arquivo}: {e}")
        else:
            print(f"  [MANTIDO]  {nome_do_arquivo}")
            arquivos_mantidos += 1

print("\n" + "="*60)
print("Limpeza Concluída.")
print(f"  Arquivos Deletados: {arquivos_deletados}")
print(f"  Arquivos Mantidos:  {arquivos_mantidos}")
print("="*60)
