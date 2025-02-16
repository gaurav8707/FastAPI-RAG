import os
from groq import Groq
from qdrant_client.models import Filter
from database import qdrant_client, documents_collection
from langchain.memory import ConversationBufferMemory
from sentence_transformers import SentenceTransformer

#
# 1) Initialize Groq client (reads API key from environment, if configured)
#
# If you need to pass the API key explicitly:
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# client = Groq(api_key=GROQ_API_KEY)
# Otherwise:
client = Groq()

#
# 2) Load the same embedding model used to store vectors
#
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

#
# 3) LangChain memory for follow-up queries
#
memory = ConversationBufferMemory()

#
# 4) Utility function to split large text into smaller chunks
#
def chunk_text(text: str, max_length: int = 1000):
    """
    Splits a string into chunks of up to max_length characters.
    Returns a list of smaller strings.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        chunks.append(text[start:end])
        start = end
    return chunks

#
# 5) Retrieve text from Qdrant & Mongo (unchanged from earlier code)
#
def retrieve_text(query: str):
    """
    Retrieve relevant documents from Qdrant based on the query embedding.
    Returns (retrieved_texts, sources).
    """
    query_vector = embedding_model.encode(query).tolist()

    search_results = qdrant_client.search(
        collection_name="documents",
        query_vector=query_vector,
        limit=3
    )

    retrieved_texts = []
    sources = []
    for result in search_results:
        payload = result.payload or {}
        doc_id = payload.get("doc_id")
        filename = payload.get("filename") or "unknown"

        if doc_id:
            doc = documents_collection.find_one({"_id": doc_id})
            if doc:
                retrieved_texts.append(doc["content"])
                sources.append(filename)

    return retrieved_texts, sources

#
# 6) Summarize text using Groq's streaming chat completions
#
def generate_summary(retrieved_texts):
    """
    Summarize a list of text strings using Groq's native Python client.
    Fix the 'ChoiceDelta' error by using '.content' instead of '.get(...)'.
    """
    if not retrieved_texts:
        return "No relevant content found."

    # Combine all retrieved texts into one prompt
    prompt_content = f"Summarize these documents into key points:\n{retrieved_texts}"

    # Prepare the chat messages
    messages = [
        {"role": "system", "content": "You are an AI summarizer."},
        {"role": "user", "content": prompt_content}
    ]

    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Your Groq model
            messages=messages,
            temperature=1,
            max_completion_tokens=1024,  # Adjust if you still hit token limits
            top_p=1,
            stream=True,
            stop=None
        )

        # Accumulate the streamed chunks into a final string
        result_text = []
        for chunk in completion:
            # chunk.choices[0].delta is a ChoiceDelta object, so use .content
            delta_content = getattr(chunk.choices[0].delta, "content", "")
            if delta_content:
                result_text.append(delta_content)

        summary = "".join(result_text).strip()
        return summary if summary else "No text returned."

    except Exception as e:
        return f"Error in summary generation: {str(e)}"

#
# 7) Main function: chat_with_documents
#    - Retrieves docs
#    - Chunks them to avoid large token usage
#    - Summarizes each chunk, then re-summarizes
#
def chat_with_documents(query: str):
    """
    1) Retrieve relevant documents from Qdrant
    2) Split large docs into smaller chunks
    3) Summarize each chunk individually
    4) (Optional) Summarize the chunk-level summaries again
    5) Return final summary & track conversation
    """
    # Load past conversation context
    conversation_history = memory.load_memory_variables({})

    retrieved_texts, sources = retrieve_text(query)
    if not retrieved_texts:
        return {"response": "No relevant documents found.", "sources": []}

    # --- CHUNKING ---
    MAX_CHUNK_SIZE = 1000  # ~1000 characters per chunk
    all_chunks = []
    for doc_text in retrieved_texts:
        doc_chunks = chunk_text(doc_text, max_length=MAX_CHUNK_SIZE)
        all_chunks.extend(doc_chunks)

    # Summarize each chunk
    chunk_summaries = []
    for chunk in all_chunks:
        summary = generate_summary([chunk])  # pass chunk as a list
        chunk_summaries.append(summary)

    # Summarize the chunk-level summaries for a final short result
    final_summary = generate_summary(chunk_summaries)

    # Combine final response
    full_response = f"Summary: {final_summary}\n\nSources: {sources}"

    # Save conversation to memory
    memory.save_context({"input": query}, {"output": full_response})

    return {
        "response": full_response,
        "sources": sources
    }
