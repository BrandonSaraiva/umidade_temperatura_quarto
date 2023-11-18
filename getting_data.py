import serial
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configuração da porta serial - certifique-se de usar a porta correta
ser = serial.Serial('COM4', 9600)  # Substitua 'COM4' pela porta serial correta

# URL da página de previsão do tempo
url = "https://weather.com/pt-BR/clima/hoje/l/d99d429a569c3150c4f12a9c12900b06f6a0c0a2fed398fc6c25ae018d0e51c8"

# Cria um arquivo CSV para armazenar os dados
csv_file = open('dados_sensor.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Escreve o cabeçalho do CSVF
csv_writer.writerow(['Data e Hora', 'Temperatura_casa (°C)',
                    'Umidade_casa (%)', 'Temperatura_real (°C)', 'Umidade_real (%)'])

try:
    while True:
        # Lê uma linha da porta serial (dados do Arduino)
        data = ser.readline().decode('latin-1').strip()  # Use 'latin-1' como codificação

        # Obtém a data e hora atual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if data.startswith("Temperatura:"):
            # Se a linha começa com "Temperatura:", atualize a temperatura da casa
            temperature_str = data.split(":")[1].strip().replace(
                "°C", "").replace("*C", "").strip()
            try:
                temperature_casa = float(temperature_str)
            except ValueError:
                print(
                    f'Erro ao converter temperatura da casa: {temperature_str}')
        elif data.startswith("Umidade:"):
            # Se a linha começa com "Umidade:" e temos uma temperatura válida, registre os dados da casa
            if temperature_casa is not None:
                humidity = float(data.split(":")[1].strip().replace("%", ""))
                try:
                    # Fazer a solicitação HTTP para a página e obter o conteúdo
                    response = requests.get(url)
                    if response.status_code == 200:
                        content = response.text
                        soup = BeautifulSoup(content, "html.parser")

                        # Encontra o elemento de temperatura
                        temperatura_element = soup.find(
                            "span", {"data-testid": "TemperatureValue"})
                        if temperatura_element:
                            temperatura_real = temperatura_element.text

                        # Encontra o elemento de umidade
                        value_elements = soup.find_all(
                            class_="CurrentConditions--tempValue--MHmYY")

                        # Verifica se há pelo menos dois elementos com a classe
                        if len(value_elements) >= 0:
                            # Pega o segundo elemento (índice 1) da lista

                            get_humidty = soup.find_all(
                                class_="WeatherDetailsListItem--wxData--kK35q")

                            umidade_real = get_humidty[2].text

                            # Escreve os dados no arquivo CSV
                            csv_writer.writerow(
                                [current_time, temperature_casa, humidity, temperatura_real, umidade_real])
                            csv_file.flush()  # Força a gravação imediata no arquivo
                            print(f'Dados registrados em {current_time}: '
                                  f'Temperatura_casa={temperature_casa}°C, Umidade_casa={humidity}%, '
                                  f'Temperatura_real={temperatura_real}, Umidade_real={umidade_real}')
                        else:
                            print(
                                "Não foi possível encontrar os dados de temperatura e umidade na página.")
                    else:
                        print(
                            f"Erro na solicitação HTTP para a página: Código de status {response.status_code}")
                except Exception as e:
                    print(f"Ocorreu um erro ao buscar dados na página: {e}")

except KeyboardInterrupt:
    pass

# Fecha a porta serial e o arquivo CSV ao interromper o programa
ser.close()
csv_file.close()
