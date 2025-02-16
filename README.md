# FastAPI-RAG 🚀  
A **Retrieval-Augmented Generation (RAG) API** using **FastAPI, Qdrant, MongoDB, and Mistral 7B (Groq API)** for document processing, semantic search, and AI-powered responses.

## 🔹 Tech Stack  
- **FastAPI** - Backend framework  
- **Qdrant** - Vector database  
- **MongoDB** - Stores metadata  
- **Mistral 7B (Groq API)** - AI model  
- **SentenceTransformers** - Generates embeddings  

## 🚀 Quick Start  
```sh
git clone https://github.com/gaurav8707/FastAPI-RAG.git
cd FastAPI-RAG
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
Create a .env file:
MONGO_URI=<your_mongodb_uri>
QDRANT_HOST=<your_qdrant_host>
GROQ_API_KEY=<your_groq_api_key>
SECRET_KEY=<your_jwt_secret>

Run the FastAPI server:

sh
Copy
Edit
uvicorn main:app --host 127.0.0.1 --port 9000 --reload
API available at http://127.0.0.1:9000/docs 🚀

📌 Key Endpoints
POST /upload/ - Upload documents
GET /search/ - Semantic search
POST /generate/ - AI-generated responses
🔥 Developed by Gaurav Sharan

sql
Copy
Edit

Now, add and push it:
```sh
echo "# FastAPI-RAG" > README.md
git add README.md
git commit -m "Added short README"
git push origin main
