from sentence_transformers import SentenceTransformer # library for generating semantic embeddings
import numpy as np # used to handle vector efficiently

model = SentenceTransformer("all-MiniLM-L6-v2") # Load the pre-trained model for generating embeddings. "all-MiniLM-L6-v2" is a compact model that provides good performance for many tasks. It generates 384-dimensional embeddings for input text.

def embed_chunks(chunks: list[str]) -> np.ndarray: # This function takes a list of text chunks and generates embeddings for each chunk using the pre-trained model. It returns a numpy array of embeddings, which are converted to float32 for efficient storage and computation. If the input list of chunks is empty, it returns an empty numpy array.
    if not chunks: 
        return np.array([])
    embeddings = model.encode(chunks, show_progress_bar = True)
    return np.array(embeddings).astype("float32")

def embed_query(query: str) -> np.ndarray: # This function takes a query string and generates an embedding for it using the same pre-trained model. It returns a numpy array of the embedding, converted to float32 for efficient storage and computation.
    embedding = model.encode([query])
    return np.array(embedding).astype("float32")