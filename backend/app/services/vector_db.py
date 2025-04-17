# app/services/vector_db.py
import chromadb  # Chroma의 Python 클라이언트 라이브러리

def init_chroma_client():
    client = chromadb.Client()  # 세부설정은 문서 참고
    return client

def store_metadata_vector(client, collection_name: str, vector, metadata: dict):
    collection = client.get_or_create_collection(collection_name)
    collection.add(
        documents=[metadata.get('text', '')],  # 혹은 원본 메타데이터의 일부
        embeddings=[vector],
        metadatas=[metadata]
    )

def search_metadata_vector(client, collection_name: str, query_vector, n_results=5):
    collection = client.get_collection(collection_name)
    results = collection.query(query_vector=query_vector, n_results=n_results)
    return results
