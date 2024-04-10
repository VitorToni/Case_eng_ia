import google.generativeai as genai


def consultar_ia(texto):
# https://aistudio.google.com/app/apikey
    genai.configure(api_key="AIzaSyCv3og6MIKTc2lPy4HZCkkClBhvIiUwG5c")

#  Checar modelos disponiveis
#      for m in genai.list_models():
#          if 'generateContent' in m.supported_generation_methods:
#              print(m.name)

    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(texto)
        return response.text
    except AttributeError as e:
        return f"Erro ao processar a resposta: {e}"
