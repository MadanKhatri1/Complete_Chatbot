from fastapi import FastAPI, UploadFile
from app.services.upload import upload_document
import uuid
from app.database.pinecone_sql_store import store_embeddings_in_pinecone_sql # type: ignore
from app.services.chat import chatbot_response

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


import os
from pathlib import Path

UPLOAD_DIR = "data"

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    filename = file.filename
    file_extension = filename.split('.')[-1].lower()
    
    # Create a unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    print(f"File saved at: {file_path}")
    
    # Get absolute path
    absolute_path = os.path.abspath(file_path)
    print(f"Absolute path: {absolute_path}")

    # Call the upload_document function
    chunks, embeddings =upload_document(file_path, "semantic")

    # Store embeddings in Pinecone and SQL
    chunk_count=store_embeddings_in_pinecone_sql(chunks, embeddings, filename, "fixed_size")

    print(f"Processed {chunk_count} chunks from the document.")

    return {"filename": filename, "saved_as": unique_filename, "file_path": file_path, "absolute_path": absolute_path}

@app.post("/chat/")
def chat_with_document(query: str,user_id: str="Demo"):
    """
    Chat with the uploaded document
    """
    
    results = chatbot_response(user_id, query, top_k=5)
    
    return {"query": query, "results": results}