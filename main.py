from fastapi import FastAPI, UploadFile, Form, HTTPException
import logging

# Import your helper functions
from file_handler import extract_text
from embeddings import store_embeddings  # sync function
from chatbot import chat_with_documents  # we assume sync

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI RAG Chatbot!"}

@app.post("/upload/")
async def upload_file(file: UploadFile, user: str = Form(...)):
    """
    Uploads a file, extracts text, and stores embeddings.
    """
    try:
        logger.info(f"Received file: {file.filename} from user: {user}")

        # 1) Extract text (this is async)
        text = await extract_text(file)

        if not text or text.startswith("Error"):
            raise HTTPException(status_code=400, detail=f"Failed to extract text: {text}")

        # 2) Store embeddings (this is sync) => NO 'await'
        store_embeddings(text, file.filename, user)

        return {"message": "File uploaded and processed successfully."}

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/chat/")
async def chat(query: str = Form(...)):
    """
    Handles chatbot queries.
    """
    try:
        # If chat_with_documents is synchronous, just call it normally
        response = chat_with_documents(query)
        return response

        # If it were async, you'd do:
        # response = await chat_with_documents(query)

    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
