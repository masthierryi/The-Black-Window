import os
import re
import time
from collections import defaultdict

# ======================================================================
#  CONFIGURAÇÃO
# ======================================================================

# 1. MODO DE SIMULAÇÃO (DRY RUN):
#    True  = Apenas simula e mostra o que seria feito, sem apagar NADA.
#    False = Realmente APAGA os arquivos duplicados.
#
#    !!!! COMECE COM True, QUANDO TIVER CERTEZA, MUDE PARA False !!!!
DRY_RUN = False

# 2. PALAVRAS-CHAVE PRIORITÁRIAS (case-insensitive)
KEYWORDS = ["mio", "cassette"]

# 3. EXTENSÕES DE MÚSICA
MUSIC_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".ogg", ".wma", ".aac"}

# ======================================================================
#  FUNÇÃO CORRIGIDA
# ======================================================================

def get_base_name(filename, extensions):
    """
    Tenta adivinhar o 'nome base' de uma música, removendo extensões,
    textos em parênteses/colchetes E NÚMEROS DE FAIXA.
    """
    nome_base, extensao = os.path.splitext(filename)
    extensao = extensao.lower()
    
    if extensao not in extensions:
        return None, False # Não é um arquivo de música

    # Passo 1: Remove (coisas) e [coisas]
    nome_limpo = re.sub(r'\[.*?\]|\(.*?\)', '', nome_base)
    
    # Passo 2 (NOVO): Remove números de faixa no início
    # ^\s* -> 0 ou mais espaços no início
    # \d+      -> 1 ou mais dígitos (ex: 02, 05)
    # [\s.-]* -> 0 ou mais espaços, pontos ou hífens (ex: ". ", " - ")
    nome_limpo = re.sub(r'^\s*\d+[\s.-]*', '', nome_limpo)
    
    # Passo 3: Limpa espaços em branco no início/fim
    nome_limpo = nome_limpo.strip()
    
    # Se o nome ficar vazio, usa o nome original (segurança)
    if not nome_limpo:
        return nome_base.strip(), True
        
    return nome_limpo, True

# ======================================================================
#  FUNÇÃO DE ESCOLHA (sem alteração)
# ======================================================================

def choose_file_to_keep(file_paths, keywords):
    """
    Decide qual arquivo (caminho completo) manter baseado nas regras.
    """
    
    preferred_files = [] # Lista de caminhos completos
    for path in file_paths:
        filename_lower = os.path.basename(path).lower()
        if any(kw in filename_lower for kw in keywords):
            preferred_files.append(path)
            
    if preferred_files:
        shortest_path = min(preferred_files, key=lambda p: len(os.path.basename(p)))
        return shortest_path
        
    shortest_path = min(file_paths, key=lambda p: len(os.path.basename(p)))
    return shortest_path

# ======================================================================
#  SCRIPT PRINCIPAL (sem alteração)
# ======================================================================

if DRY_RUN:
    print("="*60)
    print("  MODO DE SIMULAÇÃO (DRY RUN) ATIVADO")
    print("  Nenhum arquivo será deletado.")
    print("="*60 + "\n")
    time.sleep(2) 
else:
    print("="*60)
    print("  AVISO: MODO DE EXCLUSÃO REAL ATIVADO")
    print("  Arquivos serão APAGADOS PERMANENTEMENTE.")
    print("  VOCÊ TEM 5 SEGUNDOS PARA CANCELAR (Ctrl+C)")
    print("="*60 + "\n")
    try:
        for i in range(5, 0, -1):
            print(f"Iniciando em {i}...", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nOPERAÇÃO CANCELADA PELO USUÁRIO.")
        exit()

print("Iniciando varredura (incluindo subpastas)...\n")

pasta_atual = os.getcwd()
grupos = defaultdict(list)
total_deletado = 0
total_mantido = 0

try:
    NOME_DO_SCRIPT_PATH = os.path.abspath(__file__)
except NameError:
    NOME_DO_SCRIPT_PATH = os.path.abspath("deduplica_musica.py") # Fallback

# --- 1. Agrupamento (com os.walk) ---
for dirpath, dirnames, filenames in os.walk(pasta_atual):
    for filename in filenames:
        full_path = os.path.join(dirpath, filename)
        
        if os.path.abspath(full_path) == NOME_DO_SCRIPT_PATH:
            continue
            
        nome_base, eh_musica = get_base_name(filename, MUSIC_EXTENSIONS)
        
        if eh_musica:
            grupos[nome_base].append(full_path)

if not grupos:
    print("Nenhum arquivo de música foi encontrado ou agrupado.")
    print(f"Verifique se as extensões em MUSIC_EXTENSIONS estão corretas.")
    print(f"Extensões procuradas: {MUSIC_EXTENSIONS}")
    exit()

print("--- ANÁLISE DOS GRUPOS ---")

# --- 2. Processamento e Exclusão ---
for nome_base, arquivos_do_grupo in grupos.items():
    
    if len(arquivos_do_grupo) <= 1:
        total_mantido += 1
        continue
        
    print(f"\n[GRUPO: '{nome_base}'] (Encontrados {len(arquivos_do_grupo)} arquivos)")
    
    arquivo_para_manter = choose_file_to_keep(arquivos_do_grupo, KEYWORDS)
    
    for full_path in arquivos_do_grupo:
        if full_path == arquivo_para_manter:
            print(f"  [MANTER]  {full_path}")
            total_mantido += 1
        else:
            print(f"  [DELETAR] {full_path}")
            total_deletado += 1
            
            if not DRY_RUN:
                try:
                    os.remove(full_path)
                except Exception as e:
                    print(f"    ERRO AO DELETAR: {e}")

print("\n" + "="*60)
print("Processo Concluído.")
if DRY_RUN:
    print("Status: Simulação (nenhum arquivo foi alterado).")
else:
    print("Status: Execução Real Concluída.")

print(f"  Arquivos Mantidos: {total_mantido}")
print(f"  Arquivos (potencialmente) Deletados: {total_deletado}")
print("="*60)
