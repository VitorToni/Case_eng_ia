import google.generativeai as genai

def hello_world():
    genai.configure(api_key="AIzaSyBnQTuZ1dgXO_AoSIs1VbsvKEWAGA8tLbQ")

#  Checar modelos disponiveis
#      for m in genai.list_models():
#          if 'generateContent' in m.supported_generation_methods:
#              print(m.name)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content("Qual o sentido da vida?")

    return response.text