<p align="center">
  ![OIP](https://github.com/user-attachments/assets/99e60590-7bda-4f84-a207-2df143cac8f1)
</p>
<h3 align="center">RAG Chatbot</h3>

<div align="center">
  [![Status](https://img.shields.io/badge/status-active-success.svg)]() 
  [![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
</div>

<p align="center">Developed an end-to-end RAG chatbot with a FastAPI backend. The system uses MySQL to store data, Pinecone for vector search, and Redis to manage chat history and sessions. It also uses Groq for fast LLM responses, providing quick and context-aware answers.
    <br> 
</p>

## 📝 Table of Contents
- [Problem Statement](#problem_statement)
- [Idea / Solution](#idea)
- [Dependencies / Limitations](#limitations)
- [Future Scope](#future_scope)
- [Setting up a local environment](#getting_started)
- [Usage](#usage)
- [Technology Stack](#tech_stack)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## 🧐 Problem Statement <a name="problem_statement"></a>

### IDEAL
The system should provide **fast and accurate answers** from internal documents while maintaining chat history and context. It should be **scalable, reliable**, and deliver **low-latency responses** through an intelligent chatbot.

### REALITY
Current systems struggle to **retrieve relevant information** from documents and lack proper **context awareness and memory**. Manual searching is time-consuming, and existing chatbots often provide **incomplete or slow responses**.

### CONSEQUENCES
Without improvement, users **waste time searching for information**, reducing productivity and efficiency. This can lead to **higher operational costs** and **poor user experience**.

---

## 💡 Idea / Solution <a name="idea"></a>
After analyzing the ideal state, current challenges, and their consequences, a solution was designed to provide **fast, accurate, and context-aware responses**. The solution is an **end-to-end RAG-based chatbot** with a FastAPI backend.  

Key features include:  
- **Document Upload & Processing**: Users can upload documents; the system extracts and chunks text, generates embeddings, and stores them in a vector database.  
- **Conversational Memory**: Multi-turn chat context is maintained using Redis.  
- **Interview Booking**: Supports scheduling via LLM and stores booking information in Redis.  
- **Metadata Storage**: Document metadata is saved in a database for tracking.  

This approach ensures **quick, reliable, and intelligent information retrieval** for users.


## ⛓️ Dependencies / Limitations

### Dependencies
- **FastAPI**: Provides the backend API and server.  
- **Groq**: External LLM service for generating responses.  
- **Pinecone**: Vector database for storing and retrieving semantic embeddings.  
- **Redis**: In-memory store for chat history and session management.  
- **MySQL**: Relational database for storing document metadata and raw text.  
- **HuggingFace / Sentence Transformers**: Generates local embeddings before uploading to Pinecone.  
- **PyPDF**: Parses PDF documents to extract text.  

### Limitations

#### 1. Restricted File Support
- **Description**: The system only accepts PDF and TXT files.  
- **Reason**: Parsing logic uses PyPDF and standard text reading for simplicity and reliability. Complex formats like DOCX or OCR-based images were excluded to avoid adding heavy dependencies.  
- **Why it couldn’t be overcome**: Integrating libraries like python-docx or Tesseract would have increased deployment complexity and container size.  
- **Impact**: Users must convert documents to supported formats, limiting flexibility.  

#### 2. Stateless API Dependency
- **Description**: The chatbot relies on external services (Groq, Pinecone) for responses and retrieval.  
- **Reason**: These services provide state-of-the-art LLM inference and high-performance vector search without requiring local GPU resources.  
- **Why it couldn’t be overcome**: Hosting local LLMs and vector databases requires high-end hardware not available in this environment.  
- **Impact**: Service outages or high latency from external APIs could affect response times.  

#### 3. Rigid Intent Detection for Interview Booking
- **Description**: The booking feature requires explicit patterns (e.g., "name:", "email:", "date:").  
- **Reason**: Regex-based extraction ensures fast and deterministic behavior without additional LLM calls.  
- **Why it couldn’t be overcome**: Using an NLU model would add latency, reducing responsiveness in multi-turn conversations.  
- **Impact**: Users must follow strict formatting for successful booking; flexible natural conversation is not supported.  

#### 4. Short-Term Conversation Memory
- **Description**: The chatbot only remembers the last 5 messages for context.  
- **Reason**: Limiting context reduces token usage and ensures faster response times with the LLM.  
- **Why it couldn’t be overcome**: Keeping longer history risks exceeding LLM context windows, causing memory loss or API errors.  
- **Impact**: Long conversations may lose earlier context, slightly reducing multi-turn coherence.  

### Assessment & Future Research
- These limitations define the project as a **specialized, efficient assistant** rather than a fully general-purpose chatbot.  
- **Future improvements could include**:  
  - Supporting additional file formats and OCR.  
  - Replacing Regex booking with **function-calling LLMs** for flexible natural language input.  
  - Implementing **hybrid search** combining keyword + semantic retrieval for higher accuracy.

## 🚀 Future Scope <a name="future_scope"></a>

While the current version of the RAG chatbot provides fast, context-aware responses and basic interview booking, there are several features and improvements that could not be implemented during this project:  

- **Support for additional file formats**: Currently, only PDF and TXT files are supported. Future versions could include DOCX, CSV, and OCR-based image processing.  
- **Advanced natural language booking**: Replacing Regex-based extraction with function-calling LLMs would allow users to book interviews using flexible, natural conversation.  
- **Extended conversation memory**: Increasing the chat context window could improve multi-turn conversations and maintain context over longer interactions.  
- **Hybrid search**: Combining keyword-based and semantic search could improve retrieval accuracy for very specific queries.  
- **Local hosting of LLMs and vector DB**: This would reduce dependency on external services and latency, making the system fully self-contained.  
- **Enhanced analytics and dashboards**: Tracking user queries, document usage, and booking patterns for better insights and decision-making.  

With these improvements, the chatbot could evolve into a **fully general-purpose enterprise assistant**, capable of handling large-scale knowledge bases, natural conversation, and intelligent task automation across multiple domains.

## 🏁 Getting Started

These instructions will help you set up a copy of the project locally for development and testing purposes. See **Deployment** for notes on running the project in a live environment.

---

### Prerequisites

You need the following installed on your machine:  
- **Python 3.8+**  
- **Redis**  
- **MySQL**  

You will also need **API keys** for Groq and Pinecone.

# -------------------------------
# Check Python version
# Linux / Mac
python3 --version
# Windows
python --version

# -------------------------------
# Verify Redis is running
# Linux / Mac
redis-cli ping
# Output should be: PONG

# Windows (PowerShell)
redis-cli.exe ping
# Output should be: PONG

# -------------------------------
# Verify MySQL is running
# Linux
systemctl status mysql

# Mac (Homebrew)
brew services list

# Windows (PowerShell)
Get-Service -Name MySQL* 


