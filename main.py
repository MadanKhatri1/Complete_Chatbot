from fastapi import FastAPI, UploadFile
from app.services.upload import upload_document
import uuid
import os
from pathlib import Path
from app.database.pinecone_sql_store import store_embeddings_in_pinecone_sql # type: ignore
from app.services.chat import chatbot_response
from starlette.concurrency import run_in_threadpool

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



UPLOAD_DIR = "data"


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # Save file asynchronously (I/O bound - fine)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    content = await file.read()  
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # CPU-heavy work goes to thread pool 
    await run_in_threadpool(process_and_store, file_path, file.filename)
    
    return {
        "status": "processing", 
        "filename": file.filename,
        "message": "File uploaded and processing in background"
    }

def process_and_store(file_path: str, filename: str):
    """This runs in a separate thread, blocking only that thread"""
    chunks, embeddings = upload_document(file_path, "semantic")
    store_embeddings_in_pinecone_sql(chunks, embeddings, filename, "semantic")

@app.post("/chat/")
def chat_with_document(query: str,user_id:str=None):
    """
    Chat with the uploaded document
    """
    if not user_id:
        user_id = str(uuid.uuid4())  
    results = chatbot_response(user_id, query, top_k=3)
    return {
        "user_id": user_id, 
        "query": query, 
        "results": results
    }