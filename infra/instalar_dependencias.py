import os

def instalar_dependencias():
    diretorio_atual = os.path.dirname(os.path.realpath(__file__))
    caminho_requirements = os.path.join(diretorio_atual, "requirements.txt")

    # Verificar se o arquivo requirements.txt existe
    if os.path.exists(caminho_requirements):
        # Ler o arquivo requirements.txt
        with open(caminho_requirements, "r") as f:
            libs = f.read().splitlines()
            
        # Verificar se a biblioteca pode ser importada
        for lib in libs:
            try:
                __import__(lib)
            except ImportError:
                # Instalar a biblioteca se não puder ser importada
                os.system(f"pip install -q {lib}")
    else:
        print("Arquivo requirements.txt não encontrado.")