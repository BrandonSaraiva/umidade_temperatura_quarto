from elasticsearch import Elasticsearch, helpers
import json
from typing import List

def inserir_dados_elasticsearch(df, index_name, hosts=["http://localhost:9200"]):
    # Configuração do cliente Elasticsearch
    es = Elasticsearch(hosts=hosts)

    # Verifica se o índice já existe
    indice_existe = es.indices.exists(index=index_name)

    if indice_existe:
        print(f"O índice '{index_name}' já existe. Nenhum dado será inserido.")
        return

    # Converte o DataFrame para o formato desejado
    documentos = json.loads(df.to_json(
        orient="records", date_format="iso", default_handler=str))

    # Utiliza o método bulk para inserção em lote
    actions = [
        {"_op_type": "index", "_index": index_name, "_source": documento}
        for documento in documentos
    ]

    # Insere os dados no Elasticsearch
    helpers.bulk(es, actions)

    print(
        f"\nDocumentos inseridos no índice '{index_name}' com sucesso! Quantidade: {len(actions)}")

