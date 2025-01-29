# import chromadb
# from tqdm import tqdm
# from backend.embedding import chunk_text_normal, chunk_text_semantic, embed_text
# import config

# def get_chromadb_client():
#     return chromadb.PersistentClient(path=config.CHROMADB_PATH)

# def store_embeddings_in_chromadb(documents, metadata):
#     """Store text embeddings in ChromaDB."""
#     client = get_chromadb_client()
#     normal_collection = client.get_or_create_collection(name="bbc_news_normal")
#     semantic_collection = client.get_or_create_collection(name="bbc_news_semantic")

#     for i, (doc, meta) in enumerate(tqdm(zip(documents, metadata), total=len(documents))):
#         # Normal chunking
#         normal_chunks = chunk_text_normal(doc)
#         normal_embeddings = embed_text(normal_chunks)
        
#         for j, (chunk, embedding) in enumerate(zip(normal_chunks, normal_embeddings)):
#             normal_collection.add(
#                 ids=[f"normal_doc_{i}_chunk_{j}"],
#                 embeddings=[embedding],
#                 metadatas=[meta],
#                 documents=[chunk]
#             )

#         # Semantic chunking
#         semantic_chunks = chunk_text_semantic(doc)
#         semantic_embeddings = embed_text(semantic_chunks)

#         for j, (chunk, embedding) in enumerate(zip(semantic_chunks, semantic_embeddings)):
#             semantic_collection.add(
#                 ids=[f"semantic_doc_{i}_chunk_{j}"],
#                 embeddings=[embedding],
#                 metadatas=[meta],
#                 documents=[chunk]
#             )

# def retrieve_relevant_chunks(query, chunking_type, top_k=5):
#     """Retrieve most relevant chunks from ChromaDB."""
#     client = get_chromadb_client()
#     collection_name = "bbc_news_normal" if chunking_type == "normal" else "bbc_news_semantic"
#     collection = client.get_collection(name=collection_name)
    
#     query_embedding = embed_text([query])[0]
#     results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
#     return results["documents"]


import concurrent.futures
import chromadb
from tqdm import tqdm
from backend.embedding import chunk_text_normal, chunk_text_semantic, embed_text
import config

def get_chromadb_client():
    """Initialize and return ChromaDB client."""
    return chromadb.PersistentClient(path=config.CHROMADB_PATH)

def delete_existing_embeddings():
    """Delete all previous embeddings from ChromaDB."""
    client = get_chromadb_client()
    normal_collection = client.get_or_create_collection(name="bbc_news_normal")
    semantic_collection = client.get_or_create_collection(name="bbc_news_semantic")

    # Get all document IDs
    normal_docs = normal_collection.get()
    semantic_docs = semantic_collection.get()

    normal_ids = normal_docs.get("ids", [])
    semantic_ids = semantic_docs.get("ids", [])

    # Delete if IDs exist
    if normal_ids:
        normal_collection.delete(ids=normal_ids)
    if semantic_ids:
        semantic_collection.delete(ids=semantic_ids)

    print("✅ All previous embeddings deleted.")

def process_and_store_file(doc, meta, normal_collection, semantic_collection):
    """Processes and stores a single document in parallel."""
    try:
        # Normal chunking
        normal_chunks = chunk_text_normal(doc)
        normal_embeddings = embed_text(normal_chunks)  # Batch embedding

        # Store normal chunks
        for j, (chunk, embedding) in enumerate(zip(normal_chunks, normal_embeddings)):
            normal_collection.add(
                ids=[f"normal_{meta['file']}_{j}"],
                embeddings=[embedding],
                metadatas=[meta],
                documents=[chunk]
            )

        # Semantic chunking
        semantic_chunks = chunk_text_semantic(doc)
        semantic_embeddings = embed_text(semantic_chunks)

        # Store semantic chunks
        for j, (chunk, embedding) in enumerate(zip(semantic_chunks, semantic_embeddings)):
            semantic_collection.add(
                ids=[f"semantic_{meta['file']}_{j}"],
                embeddings=[embedding],
                metadatas=[meta],
                documents=[chunk]
            )
    except Exception as e:
        print(f"⚠️ Error processing {meta['file']}: {e}")

def store_embeddings_in_chromadb(documents, metadata):
    """Processes documents in parallel and stores embeddings efficiently."""
    client = get_chromadb_client()
    normal_collection = client.get_or_create_collection(name="bbc_news_normal")
    semantic_collection = client.get_or_create_collection(name="bbc_news_semantic")

    # Delete old embeddings before storing new ones
    delete_existing_embeddings()

    # Use ThreadPoolExecutor to parallelize processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_and_store_file, doc, meta, normal_collection, semantic_collection)
            for doc, meta in zip(documents, metadata)
        ]
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing Files"):
            pass  # Wait for all tasks to complete

    print("✅ All embeddings stored successfully!")

def retrieve_relevant_chunks(query, chunking_type, top_k=5):
    """Retrieve most relevant chunks from ChromaDB."""
    client = get_chromadb_client()
    collection_name = "bbc_news_normal" if chunking_type == "normal" else "bbc_news_semantic"
    collection = client.get_collection(name=collection_name)

    query_embedding = embed_text([query])[0]

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    return results["documents"]
