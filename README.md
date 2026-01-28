<p align="center">
  <a href="" rel="noopener">
 <img src="https://corp.yonyx.com/wp-content/uploads/ChatGPT-Image-Apr-29-2025-11_57_48-AM.png" alt="Project logo"></a>
</p>
<h3 align="center">RAG Chatbot</h3>

<div align="center">

  [![Hackathon](https://img.shields.io/badge/hackathon-name-orange.svg)](http://hackathon.url.com) 
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
- [Contributing](./CONTRIBUTING.md)
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

## 🏁 Getting Started  <a name="getting_started"></a>

These instructions will help you set up a copy of the project locally for development and testing purposes. See **Deployment** for notes on running the project in a live environment.
```
# Check UV version
uv --version

# Verify Redis is running (Linux / Mac)
redis-cli ping
# Output should be: PONG

# Verify Redis is running ( Windows (using PowerShell))
redis-cli.exe ping
# Output should be: PONG

# Verify MySQL is running (Linux)
systemctl status mysql

# Verify MySQL is running  ( Mac (Homebrew) )
brew services list

# Verify MySQL is running (Windows (PowerShell))
Get-Service -Name MySQL* 
```
## Installing

First, install UV ( it is lightweight, cross-platform, and built to manage Python projects and dependencies consistently)

```
yay -S uv #For Arch Linux

For Ubuntu/Debian:
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

curl -LsSf https://astral.sh/uv/install.sh | sh # For macOS

For Windows:
# Using PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# OR using pip
pip install uv
```

MySQL/MariaDB Installation

```
# For Arch Linux:
Install MariaDB (MySQL-compatible):
# Install MariaDB
sudo pacman -S mariadb

# Initialize database
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# Start and enable service
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure installation (set root password)
sudo mysql_secure_installation

Create Database and User:
# Login to MySQL
sudo mariadb -u root

# Run these SQL commands:
CREATE DATABASE mydatabase;
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON chatbot_db.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

For macOS (Homebrew):
```
# Install MySQL
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation (first time only)
mysql_secure_installation

# Create database and user
mysql -u root -p
# Then run the SQL commands above
```

For Windows:
```
1. Download MySQL Installer from mysql.com
2. Run installer, select "MySQL Server"
3. Follow setup wizard, remember root password
4. Use MySQL Workbench or command line to create database
```

Redis Installation & Setup

Installation for Arch Linux
```
# 1. Install Redis
sudo pacman -S redis

# 2. Start Redis service
sudo systemctl start redis

# 3. Enable auto-start on boot
sudo systemctl enable redis

# 4. Verify Redis is running
sudo systemctl status redis

# 5. Test connection
redis-cli ping  # Should return "PONG"

# to ensure chat history survives restarts.  
redis-cli CONFIG SET appendonly yes
redis-cli CONFIG REWRITE

```

Installation for Ubuntu/Debian:
```
# 1. Install Redis
sudo apt update
sudo apt install redis-server

# 2. Start and enable
sudo systemctl start redis
sudo systemctl enable redis

# 3. Check status
sudo systemctl status redis

# 4. Test
redis-cli ping
```

Installation for macOS (Homebrew):
```
# 1. Install Redis
brew install redis

# 2. Start Redis service
brew services start redis

# 3. Test connection
redis-cli ping
```

Installation for Windows:
```
1. Go to Microsoft Redis releases (https://github.com/microsoftarchive/redis/releases)
2. Download the latest .msi installer (Redis-x64-3.0.504.msi or newer)
3. Run the installer and follow the wizard
4. Choose "Add Redis installation folder to PATH"
5. Complete installation

Start Redis:
# Open Command Prompt or PowerShell
# Redis starts automatically as a Windows service
# Check if Redis is running
redis-server --version

# Start Redis CLI
redis-cli

# Test connection
ping
```

Run the code
```
git clone https://github.com/MadanKhatri1/Complete_Chatbot
cd Complete_Chatbot
uv pip install -r requirements.txt

# Create a .env file with API Keys with the following content
PINECONE_API_KEY="APIKEY"
GROQ_API_KEY="APIKEY"

fastapi dev main.py
```

## 🎈 Usage <a name="usage"></a>

Once the server is running, go to http://localhost:8000/docs this url. There you will see two endpoints one for uploadfile and another for chat. You first need to go to uploadfile endpoint click 'Try it out' button and upload a file (pdf or txt) and click 'Execute'. Once the upload is finished you can go to chat endpoint and again clik on 'Try it out' button then in the query input box type your question and click 'Execute' then you will see the response of the chatbot.

## ⛏️ Built With <a name = "tech_stack"></a>

- [FatAPI](https://fastapi.tiangolo.com/) - Backend
- [Groq](https://console.groq.com/home) - Chat Responses
- [Pinecone](https://www.pinecone.io/) - Store and retrieve embeddings
- [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) - Generate embeddings
- [MySQL (via PyMySQL)](https://www.mysql.com/) - Storage for data metadata
- [Redis](https://redis.io/docs/latest/) - Short-term chat history and session management
- [PyPDF](https://pypi.org/project/pypdf/) - Extracts text from PDF files
- [UV (package manager)](https://docs.astral.sh/uv/) - Fast Python package installer and resolver

## ✍️ Authors <a name = "authors"></a>
- [@MadanKhatri1](https://github.com/MadanKhatri1) 

## 🎉 Acknowledgments <a name = "acknowledgments"></a>
- [Sentence Transformers](https://www.sbert.net/) for embedding models
- [Groq](https://groq.com/) & [Pinecone](https://www.pinecone.io/) for AI infrastructure
- The open-source community for continuous inspiration


