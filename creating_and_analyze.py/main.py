import matplotlib.pyplot as plt

from geting_csvs import ler_arquivos_csv
from insert_elastic import inserir_dados_elasticsearch
from geting_index import obter_dados_elasticsearch

import pandas as pd

# Caminho para a pasta que contém os arquivos CSV
caminho_pasta = "csvs"

# Ler os arquivos CSV
df_final = ler_arquivos_csv("csvs", 1, 27)
# Name of the index
indice_elastic = "dados_temperatura_umidade"

# Inserir os dados no Elasticsearch
inserir_dados_elasticsearch(df_final, indice_elastic)

# waiting a time while the data is being inserted
print("\nwaiting a time while the data is being inserted...\n")
for i in range(0, 100000000):
    pass

# getting the data from Elasticsearch
df_elastic = obter_dados_elasticsearch(indice_elastic)
# Exibir o DataFrame
print("data frame ---> \n\n", df_elastic)

# ------------------------------------Creating the graphs------------------------------------


# # Convertendo para o formato de data e hora
df_elastic['data_e_Hora'] = pd.to_datetime(df_elastic['data_e_Hora'])

# Gráfico de Linhas Temporais para Temperatura
plt.figure(figsize=(14, 7))
plt.plot(df_elastic['data_e_Hora'],
         df_elastic['temperatura_quarto(º)'], label='Temperatura quarto')
plt.plot(df_elastic['data_e_Hora'],
         df_elastic['temperatura_real(º)'], label='Temperatura Real')

# Adicionando linhas de média
plt.axhline(y=df_elastic['temperatura_quarto(º)'].mean(),
            color='#cf4444', linestyle='--', label='Média quarto')
plt.axhline(y=df_elastic['temperatura_real(º)'].mean(),
            color='blue', linestyle='--', label='Média Real')

# Ajustando o intervalo de datas no eixo x para mostrar apenas de semana em semana
min_date = df_elastic['data_e_Hora'].min()
plt.xticks(pd.date_range(start=min_date,
           end=df_elastic['data_e_Hora'].max(), freq='W-Mon'), rotation=45)

# Ajustando o intervalo de valores nos eixos
plt.title('Variação da Temperatura ao Longo do Tempo')
plt.xlabel('Datas pegas semanalmente')
plt.ylabel('Temperatura (ºC)')
plt.legend()
plt.tight_layout()

# Adicionando legenda no canto superior esquerdo
plt.legend(loc='upper left')

plt.show()

# ------------------------------- Gráfico de Linhas Temporais para Umidade--------------------
plt.figure(figsize=(14, 7))
plt.plot(df_elastic['data_e_Hora'],
         df_elastic['umidade_quarto(%)'], label='Umidade quarto')
plt.plot(df_elastic['data_e_Hora'],
         df_elastic['umidade_real(%)'], label='Umidade Real')

# Adicionando linhas de média
plt.axhline(y=df_elastic['umidade_quarto(%)'].mean(),
            color='#cf4444', linestyle='--', label='Média quarto')
plt.axhline(y=df_elastic['umidade_real(%)'].mean(),
            color='green', linestyle='--', label='Média Real')

# Ajustando o intervalo de datas no eixo x para mostrar apenas de semana em semana
plt.xticks(pd.date_range(start=min_date,
           end=df_elastic['data_e_Hora'].max(), freq='W-Mon'), rotation=45)

plt.title('Variação da Umidade ao Longo do Tempo')
plt.xlabel('Datas pegas semanalmente')
plt.ylabel('Umidade (%)')
plt.legend()
plt.tight_layout()

# Adicionando legenda no canto superior esquerdo
plt.legend(loc='upper left')

plt.show()

# # ----------Graficos de barra sobre dias da semana e temperatura------------

# Criando uma nova coluna para o dia da semana
df_elastic['Dia_da_Semana'] = df_elastic['data_e_Hora'].dt.day_name()

# Calculando a média de temperatura para cada dia da semana (quarto)
media_temperatura_quarto_por_dia = df_elastic.groupby(
    'Dia_da_Semana')['temperatura_quarto(º)'].mean()

# Calculando a média de temperatura para cada dia da semana (real)
media_temperatura_real_por_dia = df_elastic.groupby(
    'Dia_da_Semana')['temperatura_real(º)'].mean()

# Ordenando os dias da semana
ordem_dias = ['Monday', 'Tuesday', 'Wednesday',
              'Thursday', 'Friday', 'Saturday', 'Sunday']
media_temperatura_quarto_por_dia = media_temperatura_quarto_por_dia.reindex(
    ordem_dias)
media_temperatura_real_por_dia = media_temperatura_real_por_dia.reindex(
    ordem_dias)

# Gráfico de Barras para Média de Temperatura (quarto) por Dia da Semana
plt.figure(figsize=(14, 7))

# Subplot com 1 linha, 2 colunas, posição 1
plt.subplot(1, 2, 1)
media_temperatura_quarto_por_dia.plot(kind='bar', color='#cf4444')

plt.title('Média de Temperatura (quarto) por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Média de Temperatura (ºC)')
plt.xticks(rotation=45)

# Gráfico de Barras para Média de Temperatura (Real) por Dia da Semana
plt.subplot(1, 2, 2)  # Subplot com 1 linha, 2 colunas, posição 2
media_temperatura_real_por_dia.plot(kind='bar', color='#c68021')
plt.title('Média de Temperatura (Real) por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Média de Temperatura (ºC)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ------------Graficos de barra os horarios e temperatura------------

# Extraia a hora do dia como uma nova coluna
df_elastic['hora_do_dia'] = df_elastic['data_e_Hora'].dt.hour

# Ordene os DataFrames pelos horários do dia
media_temperatura_quarto_por_hora = df_elastic.groupby(
    'hora_do_dia')['temperatura_quarto(º)'].mean().sort_index()
media_temperatura_real_por_hora = df_elastic.groupby(
    'hora_do_dia')['temperatura_real(º)'].mean().sort_index()

# pegando os top 3 horarios mais quentes e frios
top_quentes_quarto = media_temperatura_quarto_por_hora.nlargest(3)
top_frios_quarto = media_temperatura_quarto_por_hora.nsmallest(3)
top_quentes_real = media_temperatura_real_por_hora.nlargest(3)
top_frios_real = media_temperatura_real_por_hora.nsmallest(3)

# Sort the top_quentes_quarto and top_frios_quarto by the 'hora_do_dia' column
top_quentes_quarto = top_quentes_quarto.sort_index()
top_frios_quarto = top_frios_quarto.sort_index()

# Sort the top_quentes_real and top_frios_real by the 'hora_do_dia' column
top_quentes_real = top_quentes_real.sort_index()
top_frios_real = top_frios_real.sort_index()

# Crie o gráfico de barras para os top 3 horários mais Quentes e Frios (quarto)
plt.figure(figsize=(18, 9))

# Subplots para os Horários mais Quentes (quarto)
plt.subplot(2, 2, 1)
top_quentes_quarto.plot(kind='bar', color='#cf4444', label='Mais Quentes')
plt.title('top 3 horários mais Quentes (quarto)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Temperatura (ºC)')
plt.xticks(rotation=0)

# Subplots para os Horários mais Frios (quarto)
plt.subplot(2, 2, 2)
top_frios_quarto.plot(kind='bar', color='#cb6969', label='Mais Frios')
plt.title('top 3 horários mais Frios (quarto)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Temperatura (ºC)')
plt.xticks(rotation=0)

# Subplots para os Horários mais Quentes (real)
plt.subplot(2, 2, 3)
top_quentes_real.plot(kind='bar', color='orange', label='Mais Quentes')
plt.title('top 3 horários mais Quentes (Real)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Temperatura (ºC)')
plt.xticks(rotation=0)

# Subplots para os Horários mais Frios (real)
plt.subplot(2, 2, 4)
top_frios_real.plot(kind='bar', color='#c68021', label='Mais Frios')
plt.title('top 3 horários mais Frios (Real)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Temperatura (ºC)')
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ------------Graficos de barra os horarios e umidade------------

# Extraia a hora do dia como uma nova coluna
df_elastic['hora_do_dia'] = df_elastic['data_e_Hora'].dt.hour

# Ordene os DataFrames pelos horários do dia
media_umidade_quarto_por_hora = df_elastic.groupby(
    'hora_do_dia')['umidade_quarto(%)'].mean().sort_index()
media_umidade_real_por_hora = df_elastic.groupby(
    'hora_do_dia')['umidade_real(%)'].mean().sort_index()

top_umidos_quarto = media_umidade_quarto_por_hora.nlargest(3)
top_secos_quarto = media_umidade_quarto_por_hora.nsmallest(3)
top_umidos_real = media_umidade_real_por_hora.nlargest(3)
top_secos_real = media_umidade_real_por_hora.nsmallest(3)

# Sort the top_umidos_quarto and top_secos_quarto by the 'hora_do_dia' column
top_umidos_quarto = top_umidos_quarto.sort_index()
top_secos_quarto = top_secos_quarto.sort_index()

# Sort the top_umidos_real and top_secos_real by the 'hora_do_dia' column
top_umidos_real = top_umidos_real.sort_index()
top_secos_real = top_secos_real.sort_index()

# Crie o gráfico de barras para os top 3 horários mais Úmidos e Secos (quarto)
plt.figure(figsize=(18, 9))

# Subplots para os Horários mais Úmidos (quarto)
plt.subplot(2, 2, 1)
top_umidos_quarto.plot(kind='bar', color='#cb6969', label='Mais Úmidos')
plt.title('top 3 horários mais Úmidos (quarto)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Umidade (%)')
plt.xticks(rotation=0)

# Subplots para os Horários mais Secos (quarto)
plt.subplot(2, 2, 2)
top_secos_quarto.plot(kind='bar', color='#cf4444', label='Mais Secos')
plt.title('top 3 horários mais Secos (quarto)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Umidade (%)')
plt.xticks(rotation=0)

# Subplots para os Horários mais Úmidos (real)
plt.subplot(2, 2, 3)
top_umidos_real.plot(kind='bar', color='#c68021', label='Mais Úmidos')
plt.title('top 3 horários mais Úmidos (Real)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Umidade (%)')
plt.xticks(rotation=0)

# Subplots para os Horários mais Secos (real)
plt.subplot(2, 2, 4)
top_secos_real.plot(kind='bar', color='orange', label='Mais Secos')
plt.title('top 3 horários mais Secos (Real)')
plt.xlabel('Hora do Dia')
plt.ylabel('Média de Umidade (%)')
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()
