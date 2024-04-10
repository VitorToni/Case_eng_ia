import os

def instalar_dependencias():
    diretorio_atual = os.path.dirname(os.path.realpath(__file__))
    caminho_requirements = os.path.join(diretorio_atual, 'requirements.txt')
    
    print(caminho_requirements)
    if os.path.exists(caminho_requirements):
        os.system(f'pip install -q -r {caminho_requirements}')
    else:
        print('Arquivo requirements.txt não encontrado.')
