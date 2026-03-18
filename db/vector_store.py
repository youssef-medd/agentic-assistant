import hashlib
import chromadb
from chromadb.config import Settings
import ollama
_client = chromadb.PersistentClient(
    path = "./chroma_db" ,
    settings = Settings(anonymized_telemetry = False))
def _get_collection(user_id):
    return _client.get_or_create_collection(
        name = f"user_{user_id}",
        metadata = {"hnsw:space" : "cosine"}
    )
def _embed(text):
    return ollama.embeddings(model = "nomic-embed-text" , prompt = text)["embedding"]
def _chunk(text , size = 400 , overlap = 60):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i+ size]))
        i += size - overlap
    return [c for c in chunks if c.strip()]
def ingest_document(user_id , text , filename , filetype = "pdf"):
    if not text or not text.strip():
        return 0
    collection = _get_collection(user_id)
    chunks = _chunk(text)
    ids , embeddings , documents , metadatas = [] , [] , [] ,[]
    for i , chunk in enumerate(chunks):
        chunk_id = hashlib.md5(f"{user_id}:{filename}:{i}".encode()).hexdigest()
        ids.append(chunk_id)
        embeddings.append(_embed(chunk))
        documents.append(chunk)
        metadatas.append({
            "user_id" : user_id,
            "filename" : filename,
            "filetype" : filetype ,
            "chunk_index" : i
        })
    collection.upsert(ids = ids , embeddings=embeddings , documents=documents , metadatas=metadatas)
    return len(chunks)
def query_documents(user_id , query , n_results = 5):
    collection = _get_collection(user_id)
    if collection.count() == 0 :
        return []
    n = min(n_results , collection.count())
    results = collection.query(
        query_embeddings=[_embed(query)],
        n_results= n,
        include=[ "documents" , "metadatas" , "distances"]
    )
    hits = []
    for doc , meta , dist in zip(results["documents"][0],
                                 results["metadatas"][0],
                                 results["distances"][0]
    ):
        hits.append({
            "text" : doc ,
            "source" : meta.get("filename"),
            "score" : round( - dist ,3)
        })
    return hits
def list_user_documents(user_id):
    try :
        collection = _get_collection(user_id)
        results = collection.get(include=["metadatas"])
        return sorted({m["filename"] for m in results["metadatas"]})
    except Exception :
        return []
def save_message(user_id: str, role: str, content: str):
    """
    Save every chat message to ChromaDB.
    role is either "user" or "assistant"
    """
    collection = _get_collection(user_id)
    
    import time
    msg_id = hashlib.md5(f"{user_id}:{role}:{content}:{time.time()}".encode()).hexdigest()
    
    collection.upsert(
        ids=[msg_id],
        embeddings=[_embed(content)],
        documents=[content],
        metadatas=[{
            "user_id":   user_id,
            "role":      role,       
            "type":      "message",  
            "filename":  "chat",
            "timestamp": str(time.time()),
        }]
    )




    