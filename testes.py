import requests
from bs4 import BeautifulSoup

# URL da página de previsão do tempo
url = "https://weather.com/pt-BR/clima/horaria/l/d99d429a569c3150c4f12a9c12900b06f6a0c0a2fed398fc6c25ae018d0e51c8"

# Faz a solicitação HTTP
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra o elemento de temperatura
    temperatura_element = soup.find("span", {"data-testid": "TemperatureValue"})
    if temperatura_element:
        temperatura = temperatura_element.text
        

    # Encontra o elemento de umidade
    value_elements = soup.find_all(class_="DetailsTable--value--2YD0-")

    # Verifica se há pelo menos dois elementos com a classe
    if len(value_elements) >= 2:
        # Pega o segundo elemento (índice 1) da lista
        umidade = value_elements[2].text

    # Imprime os valores de temperatura e umidade
    print(f"Temperatura: {temperatura}")
    print(f"Umidade: {umidade}")
else:
    print("Não foi possível acessar a página")

