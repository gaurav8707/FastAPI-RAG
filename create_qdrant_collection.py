from database import qdrant_client
from qdrant_client.models import Distance, VectorParams

# Check if the collection already exists
collections = qdrant_client.get_collections()
collection_names = [c.name for c in collections.collections]

if "documents" not in collection_names:
    print("⚡ Creating Qdrant collection: 'documents'...")

    # Create a collection with 384-dimensional vectors (adjust if needed)
    qdrant_client.create_collection(
        collection_name="documents",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # Ensure this matches your embedding model
    )

    print("✅ Qdrant collection 'documents' created successfully.")
else:
    print("✅ Qdrant collection 'documents' already exists.")
