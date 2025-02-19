# 🚀 FastAPI-RAG  
A **powerful AI-powered Retrieval-Augmented Generation (RAG) API** that allows you to **upload documents, search content using semantic embeddings, and generate AI responses** using **FastAPI, Qdrant, MongoDB, and Mistral 7B (via Groq API).**  

## 🌟 Features  
✅ Upload and store documents  
✅ Perform **semantic search** on documents  
✅ Generate **AI-powered responses** based on stored content  
✅ Fast and scalable with **FastAPI** and **vector search**  

## 🛠️ Technologies Used  
- **FastAPI** - Backend API framework  
- **Qdrant** - High-performance vector database  
- **MongoDB** - Stores document metadata  
- **Mistral 7B (Groq API)** - AI model for response generation  
- **SentenceTransformers** - Generates text embeddings for search  

## 🚀 Getting Started  

### 1️⃣ Clone the Repository  
```sh  
git clone https://github.com/gaurav8707/FastAPI-RAG.git  
cd FastAPI-RAG  
```

### 2️⃣ Set Up the Environment  
```sh  
python -m venv env  
source env/bin/activate  # On Windows: env\Scripts\activate  
pip install -r requirements.txt  
```

### 3️⃣ Configure Environment Variables  
Create a `.env` file in the project directory with:  
```ini  
MONGO_URI=<your_mongodb_uri>  
QDRANT_HOST=<your_qdrant_host>  
GROQ_API_KEY=<your_groq_api_key>  
SECRET_KEY=<your_jwt_secret>  
```

### 4️⃣ Start the FastAPI Server  
```sh  
uvicorn main:app --host 127.0.0.1 --port 9000 --reload  
```
📌 **API Docs:** [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)  

---

## 🌍 API Endpoints  
🔹 **`POST /upload/`** - Upload a document  
🔹 **`GET /search/`** - Search documents using embeddings  
🔹 **`POST /generate/`** - AI-generated responses based on content  

## 📌 Why Use FastAPI-RAG?  
💡 **Advanced AI Responses** - Uses **Mistral 7B** for intelligent generation  
⚡ **Blazing Fast API** - Built with **FastAPI** for speed  
🔍 **Powerful Search** - Uses **vector search** for **semantic matching**  
📂 **Multi-Document Support** - Upload multiple documents and search instantly  

---
# FastAPI Working Demo

📽️ **Watch the Demo Video:** [Click here](https://youtu.be/zHR87trQVzU)


## 🎯 Contributing  
Want to improve FastAPI-RAG? Fork the repo, create a branch, and submit a PR!  

---

## 👨‍💻 Developed By  
🚀 **Gaurav Sharan**  

---

### 📢 Star ⭐ this repo if you find it useful!  
Made with ❤️ for AI & NLP Enthusiasts! 🚀  
