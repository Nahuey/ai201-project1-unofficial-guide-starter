import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Embedding function and ChromaDB client are initialized once at module load.
# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used by app.py during ingestion."""
    return _collection


def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in the vector database.

    This function is already implemented — read through it before moving on.

    _collection.add() takes three parallel lists built from the chunks
    returned by chunk_document():
      - documents : raw text strings — ChromaDB's embedding function converts
                    these to vectors automatically using sentence-transformers
      - metadatas : one dict per chunk, stored alongside the vector so that
                    retrieve() can surface which game a result came from
      - ids       : the unique chunk_id strings used to identify each entry

    You don't generate embeddings manually here — you hand over the text
    and ChromaDB handles the vector math.
    """
    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"title": c["title"]} for c in chunks],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, distance_threshold=0.6):
    collection = get_collection()
    
    # 1. Execute the standard search
    search_kwargs = {
        "query_texts": [query],
        "n_results": 4
    }
    
    # If you implemented the LLM router from the previous step, 
    # your metadata filter ('where' clause) would be added here.
    
    raw_results = collection.query(**search_kwargs)
    
    # 2. Extract the lists (index 0 because we only passed one query string)
    documents = raw_results['documents'][0]
    distances = raw_results['distances'][0]
    metadatas = raw_results['metadatas'][0]
    
    # 3. Filter the results
    filtered_chunks = []
    for i in range(len(distances)):
        # Lower distance means higher similarity
        if distances[i] <= distance_threshold:
            filtered_chunks.append({
                "text": documents[i],
                "metadata": metadatas[i],
                "distance": distances[i]
            })
            
    # --- Console Feedback for Testing ---
    print(f"\nQuery: '{query}'")
    print(f"--> Found {len(distances)} total chunks.")
    print(f"--> Kept {len(filtered_chunks)} chunks under the {distance_threshold} threshold.")
    for chunk in filtered_chunks:
        print(f"  - [{chunk['metadata']['title']}] (dist: {chunk['distance']:.3f})")
    # ------------------------------------
    for chunk in filtered_chunks:
        print(f"[{chunk['metadata']}] (dist: {chunk['distance']:.3f}) \n{chunk['text']}\n")
    # Return only the highly relevant chunks to feed into your LLM
    return filtered_chunks