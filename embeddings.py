from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct
import uuid
from database import qdrant_client, documents_collection

model = SentenceTransformer("all-MiniLM-L6-v2")  # or your chosen model

def store_embeddings(text, filename, user):
    """Synchronous function to store embeddings in Qdrant + metadata in MongoDB."""
    doc_id = str(uuid.uuid4())
    vector = model.encode(text).tolist()

    # Store metadata in MongoDB
    documents_collection.insert_one({
        "_id": doc_id,
        "filename": filename,
        "content": text,
        "user": user
    })

    # Store embeddings in Qdrant
    qdrant_client.upsert(
        collection_name="documents",
        points=[PointStruct(
            id=doc_id,
            vector=vector,
            payload={"doc_id": doc_id, "filename": filename}
        )]
    )
