from pypdf import PdfReader # type: ignore
import re
from typing import List, Literal
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Load model once at module level (simplest singleton)
_embedding_model = None

def get_embedding_model():
    """Get or create the embedding model (lazy loading)"""
    global _embedding_model
    if _embedding_model is None:
        print("Loading embedding model...")
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Embedding model loaded")
    return _embedding_model

def encode_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for list of texts
    """
    model = get_embedding_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return embeddings.tolist()
    

def document_processing(file_path:str="..data/sample.pdf"):
    
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        page_texts = [page.extract_text() for page in reader.pages]
        text = "\n".join(page_texts) 

    if file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read()

    return text


def semantic_chunk(text: str, threshold: float = 0.75) -> List[str]:
    """
    Chunk text based on semantic similarity between sentences.

    Parameters
    ----------
    text : str
        Input text
    threshold : float
        Cosine similarity threshold (0–1)
    """
    if not text.strip():
        return []

    # Sentence splitting (simple but effective)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    if len(sentences) == 1:
        return sentences

    model = get_embedding_model()
    embeddings = model.encode(
        sentences,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    chunks: List[str] = []
    current_chunk: List[str] = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = cosine_similarity(
            [embeddings[i - 1]],
            [embeddings[i]]
        )[0][0]

        if similarity >= threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    # Append last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def fixed_size_chunk(text: str, chunk_size: int = 500) -> List[str]:
    """
    Chunk text into fixed-size character windows.
    """
    if not text.strip():
        return []

    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

def chunk_text(
    text: str,
    strategy: Literal["fixed_size", "semantic"] = "fixed_size",
    chunk_size: int = 500,
    threshold: float = 0.75
) -> List[str]:
    """
    Chunk text using selected strategy.

    Parameters
    ----------
    text : str
        Input text
    strategy : "fixed_size" | "semantic"
    chunk_size : int
        Used only for fixed_size strategy
    threshold : float
        Used only for semantic strategy
    """
    if strategy == "fixed_size":
        return fixed_size_chunk(text, chunk_size=chunk_size)

    if strategy == "semantic":
        return semantic_chunk(text, threshold=threshold)

    raise ValueError(f"Unknown chunking strategy: {strategy}")
    

# Global function to get embeddings (easy interface)
def get_embeddings(text_chunks: List[str]) -> List[List[float]]:
    model = get_embedding_model()  
    embeddings = model.encode(text_chunks)
    return embeddings


def upload_document(file_path: str,strategy:str):
    text = document_processing(file_path)
    chunks = chunk_text(text, strategy=strategy)
    embeddings = get_embeddings(chunks)
    return chunks, embeddings


if __name__ == "__main__":
    document_processing()