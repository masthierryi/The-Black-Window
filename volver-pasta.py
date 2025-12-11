import os
import shutil

# Pega o caminho da pasta atual onde o script está sendo executado.
pasta_atual = os.getcwd()
print(f"Organizando arquivos na pasta: {pasta_atual}\n")

# Cria uma lista de arquivos que já estão na pasta principal para não sobrescrevê-los.
# Inclui o próprio script para que ele não seja considerado um arquivo a ser movido.
arquivos_na_raiz = {
    f for f in os.listdir(pasta_atual) 
    if os.path.isfile(os.path.join(pasta_atual, f))
}

# Percorre todos os itens (arquivos e pastas) na pasta atual.
for nome_do_item in os.listdir(pasta_atual):
    caminho_do_item = os.path.join(pasta_atual, nome_do_item)
    
    # Se o item for uma pasta (uma das F_i), entra nela.
    if os.path.isdir(caminho_do_item):
        print(f"--- Lendo a subpasta: {nome_do_item} ---")
        
        # Percorre os arquivos dentro da subpasta.
        for nome_do_arquivo in os.listdir(caminho_do_item):
            caminho_origem = os.path.join(caminho_do_item, nome_do_arquivo)
            
            # Verifica se é um arquivo de verdade.
            if os.path.isfile(caminho_origem):
                
                # Se o arquivo já existir na pasta principal, avisa e pula.
                if nome_do_arquivo in arquivos_na_raiz:
                    print(f"  -> [IGNORADO] O arquivo '{nome_do_arquivo}' já existe no destino.")
                
                # Se não existir, move o arquivo.
                else:
                    print(f"  -> [MOVENDO] '{nome_do_arquivo}'...")
                    caminho_destino = os.path.join(pasta_atual, nome_do_arquivo)
                    shutil.move(caminho_origem, caminho_destino)
                    
                    # Adiciona o nome do arquivo à lista para não ser sobrescrito por outro igual.
                    arquivos_na_raiz.add(nome_do_arquivo)
                    
print("\nProcesso concluído.")