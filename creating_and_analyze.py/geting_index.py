from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd

def obter_dados_elasticsearch(indice: str) -> pd.DataFrame:
    # Conectar-se ao servidor Elasticsearch (certifique-se de que o Elasticsearch está em execução)
    # Atualize com as configurações do seu Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    # Consulta para obter todos os documentos no índice especificado
    resultados = scan(es, index=indice)

    # Extrair chaves e valores dos documentos
    dados = []
    for hit in resultados:
        source = hit['_source']
        dados.append(source)
        
    # Criar DataFrame a partir dos dados extraídos
    df = pd.DataFrame(dados)

    return df
