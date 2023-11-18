import os
import pandas as pd
import chardet

def ler_arquivos_csv(caminho_pasta, inicio, fim):
    dados_completos = []

    for i in range(inicio, fim):
        nome_arquivo = f"{i}.csv"
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

        if os.path.exists(caminho_arquivo):
            # Detect the encoding of the CSV file
            with open(caminho_arquivo, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']

            # Read the CSV file using the detected encoding
            dados = pd.read_csv(caminho_arquivo, encoding=encoding)

            # Convert all data to UTF-8
            for col in dados.columns:
                if dados[col].dtype == 'object':
                    dados[col] = dados[col].map(lambda x: x.encode(
                        'utf-8').decode('utf-8') if isinstance(x, str) else x)

            # Corrige os caracteres indesejados nos dados
            dados.columns = [col.replace('°', '') for col in dados.columns]
            dados.columns = [col.replace('%', '') for col in dados.columns]

            # Extrai os números dos dados convertendo para string e removendo caracteres não numéricos
            if 'Temperatura_real (C)' in dados.columns:
                dados['Temperatura_real (C)'] = dados['Temperatura_real (C)'].str.extract(
                    '(\d+)').astype(float)
            if 'Umidade_real (%)' in dados.columns:
                dados['Umidade_real (%)'] = dados['Umidade_real (%)'].str.extract(
                    '(\d+)').astype(float)

            # Adiciona os dados corrigidos à lista
            dados_completos.append(dados)

    # Concatena todos os DataFrames na lista em um único DataFrame
    dados_completos = pd.concat(dados_completos, ignore_index=True)

    # Remove as 2 ultimas colunas
    dados_completos = dados_completos.iloc[:, :-2]

    # Renomeia as colunas para ser aceito no elastic
    dados_completos.columns = [
        'data_e_Hora', 'temperatura_quarto(º)', 'umidade_quarto(%)', 'temperatura_real(º)', 'umidade_real(%)']

    # removing the % of the values of the column umidade_real(%)
    dados_completos['umidade_real(%)'] = dados_completos['umidade_real(%)'].str.extract(
        '(\d+)').astype(float)

    # Retorna o DataFrame com os nomes das colunas modificados
    return dados_completos
