import google.generativeai as genai
import logging

def consultar_google(texto):
    """
    Consulta o Google AI Studio para gerar conteúdo baseado no texto fornecido.

    Args:
        texto (str): O texto base para a geração de conteúdo.

    Returns:
        str: O conteúdo gerado pelo modelo.
    """
    
    logger = logging.getLogger(__name__)

    # Crie sua key:
    # https://aistudio.google.com/app/apikey
    genai.configure(api_key="")

    # Checar modelos disponiveis
    # for m in genai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print(m.name)

    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(texto)
        return response.text
    except AttributeError as e:
        logger.error(f"Erro ao processar a resposta: {e}")
        return None
