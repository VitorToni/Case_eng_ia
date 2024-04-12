import os
import logging

def instalar_dependencias():
    """
    Verifica e instala as dependências listadas no arquivo requirements.txt.

    """

    logger = logging.getLogger(__name__)
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
                __import__(f"{lib}")
            except ImportError:
                # Instalar a biblioteca se não puder ser importada
                try:
                    os.system(f"pip install -q {lib}")
                    logger.info(f"Instalou a biblioteca {lib}.")
                except Exception as e:
                    logger.error(f"Erro ao instalar a biblioteca {lib}: {e}")
                    raise e
    else:
        logger.error("Arquivo requirements.txt não encontrado.")
