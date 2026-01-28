import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from typing import List
import json
from app.redis.chat_memory import add_message, get_recent_messages
from groq import Groq  # Groq client
import re 
from app.redis.bookings import save_booking
# Load environment variables
load_dotenv()

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
index_name = "chatbotintern"
pinecone = Pinecone(api_key=PINECONE_API_KEY)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

_embedding_model = None

def get_embedding_model():
    """Lazy load HuggingFace sentence transformer model"""
    global _embedding_model
    if _embedding_model is None:
        print("Loading HuggingFace embedding model...")
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded")
    return _embedding_model

def encode_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for list of texts"""
    model = get_embedding_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return embeddings.tolist()

def search_text_from_pinecone(query: str, top_k: int = 5):
    """
    Search Pinecone and fetch text chunks directly from metadata.
    """
    index = pinecone.Index(index_name)

    # Encode query
    query_embedding = encode_texts([query])[0]

    # Query Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # Collect results
    output = []
    for match in results.matches:
        output.append({
            "id": match.id,
            "score": match.score,
            "text": match.metadata.get("text", ""),
            "filename": match.metadata.get("filename"),
            "chunk_index": match.metadata.get("chunk_index"),
            "strategy": match.metadata.get("chunk_strategy"),
            "chunk_size": match.metadata.get("chunk_size"),
            "preview": match.metadata.get("text", "")[:200] + "..."
                if len(match.metadata.get("text", "")) > 200 else match.metadata.get("text", "")
        })

    combined_text = "\n\n".join([item["text"] for item in output if item["text"]])

    return combined_text

def extract_booking_with_llm(query: str):
    prompt = f"""Extract name, email, date, time from this booking request.
    Return ONLY JSON: {{"name": "...", "email": "...", "date": "YYYY-MM-DD", "time": "HH:MM"}}
    If missing, use null.
    Request: {query}"""
    
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    try:
        result = json.loads(response.choices[0].message.content)
        if result.get("email") and result.get("date"):
            return result
    except:
        pass
    return None

def chatbot_response(user_id: str, query: str, top_k: int = 3):
    try:
        """
        Generate chatbot response using recent chat history, Pinecone search results,
        and Groq chat model. Supports interview booking.
        """

        # Store user query in Redis
        add_message(user_id, f"User: {query}")

        booking = extract_booking_with_llm(query)
        if booking:
            save_booking(user_id, booking)
            return f"Booked for {booking['name']} on {booking['date']} at {booking['time']}"

        
        recent_messages = get_recent_messages(user_id, limit=3)
        context = "\n".join(recent_messages)

        if len(context) > 1000:  
            context = context[-1000:]

        search_results = search_text_from_pinecone(query, top_k=top_k)

        system_prompt = f"""
        You are a helpful assistant.

        Rules:
        - Use BOTH the previous chat context and the Pinecone search results.
        - If the answer is not in the context or search results, say "I don't know".
        - Be concise and accurate.
        - Cite sources using filenames when possible.

        Previous Chat Context:
        {context}

        Search Results:
        {search_results}
        """

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.2
        )

        final_answer = response.choices[0].message.content
        add_message(user_id, f"Bot: {final_answer}")

        return final_answer
    
    except Exception as e:
        return f"Error: {str(e)}"
