from pinecone import Pinecone, ServerlessSpec # type: ignore
from dotenv import load_dotenv
import os
import pymysql
from typing import List
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "chatbotintern"


def store_embeddings_in_pinecone_sql(chunks: List[str], embeddings: List[List[float]], filename: str, strategy: str):
    """
    Store document chunks with embeddings in Pinecone
    
    Args:
        chunks: List of text chunks
        embeddings: List of embedding vectors
        filename: Original filename
        strategy: Chunking strategy used
    """
    # Check if index exists
    existing_indexes = [index.name for index in pc.list_indexes()]

    if index_name not in existing_indexes:
        # Get dimension from first embedding
        dimension = len(embeddings[0]) if embeddings else 384
        
        pc.create_index(
            name=index_name,
            dimension=dimension,  
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Created index: {index_name} (dimension: {dimension})")
    else:
        print(f"Index already exists: {index_name}")

    # Connect to the index
    index = pc.Index(index_name)
    
    # Prepare vectors for Pinecone
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        # Create unique ID
        chunk_id = f"{filename}_{i}_{hash(chunk) % 10000}"

        truncated_text = chunk[:5000] if len(chunk) > 5000 else chunk

        
        vectors.append({
            "id": chunk_id,
            "values": embedding,
            "metadata": {
                "text":chunk,
                "filename": filename,
                "chunk_index": i,
                "chunk_strategy": strategy,
                "chunk_size": len(chunk),
                "embedding_dim": len(embedding)
            }
        })
    
    # Upload in batches (Pinecone limit: 100 vectors per upsert)
    batch_size = 100
    total_stored = 0
    
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        total_stored += len(batch)
        print(f"  Uploaded batch {i//batch_size + 1}: {len(batch)} vectors")
    
    print(f"Total stored: {total_stored} vectors from {filename}")

    try:
        conn = pymysql.connect(
            host='localhost',
            user='madan',
            password='12349',
            database='mydatabase',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with conn.cursor() as cursor:
            # Create table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    filename VARCHAR(255),
                    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    chunks_count INT,
                    strategy VARCHAR(50),
                    chunks LONGTEXT
                )
            ''')
            
            # Insert data
            sql = "INSERT INTO documents (filename, chunks_count, strategy, chunks) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (filename, len(chunks), strategy, str(chunks)))
        conn.commit()
        conn.close()
        print(f"MySQL: Saved metadata for {filename}")
        
    except Exception as e:
        print(f"MySQL error: {e}")



    return total_stored