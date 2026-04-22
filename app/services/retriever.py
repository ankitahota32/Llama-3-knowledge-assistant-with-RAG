import faiss
import json
import numpy as np
from app.config import settings
import os

INDEX_PATH = os.path.join(settings.VECTOR_STORE_PATH, "index.faiss") # Define the path to the FAISS index file, which will store the vector representations of the text chunks for efficient similarity search. The path is constructed using the VECTOR_STORE_PATH from the settings and naming the file "index.faiss".
CHUNKS_PATH = os.path.join(settings.VECTOR_STORE_PATH, "chunks.json") # Define the path to the JSON file that will store the original text chunks corresponding to the embeddings in the FAISS index. This allows us to retrieve the original text when we get results from the index. The path is constructed using the VECTOR_STORE_PATH from the settings and naming the file "chunks.json".

def save_to_index(chunks: list[str], embeddings: np.ndarray): # This function takes a list of text chunks and their corresponding embeddings, and saves them to the FAISS index and the JSON file. It first checks if the index already exists; if it does, it loads the existing index and chunks. Then it adds the new embeddings to the index and updates the JSON file with the new chunks. Finally, it prints out how many chunks were saved and the total number of chunks in the index.
    dim = embeddings.shape[1] # Get the dimensionality of the embeddings, which is needed to create the FAISS index. This assumes that the embeddings are in a 2D array where each row corresponds to a chunk and each column corresponds to a dimension of the embedding.
    
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "r") as f:
            existing_chunks = json.load(f)
    else:
        index = faiss.IndexFlatL2(dim)
        existing_chunks = []
        
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH) # Save the updated index to disk. This will overwrite the existing index file with the new one that includes the added embeddings.
    
    all_chunks = existing_chunks + chunks # append new chunks
    with open(CHUNKS_PATH, "w") as f: # Save the updated list of chunks to the JSON file. This will overwrite the existing file with the new list that includes the appended chunks.
        json.dump(all_chunks, f)
        
    print(f"Saved {len(chunks)} chunks. Total: {len(all_chunks)}")
    
def search_index(query_embedding: np.ndarray, k: int = 4) -> list[str]: # finds the k most relevant chunks
    if not os.path.exists(INDEX_PATH):
        return []
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "r") as f:
        chunks = json.load(f)
        
    D, I = index.search(query_embedding, k) # Perform a search on the FAISS index using the query embedding. This will return the distances (D) and the indices (I) of the k nearest neighbors in the index. The indices correspond to the positions of the chunks in the original list of chunks.
    results = [chunks[i] for i in I[0] if i < len(chunks)] # Retrieve the original text chunks corresponding to the indices returned by the search. This list comprehension iterates over the indices in I[0] (the first row of the indices returned by the search) and retrieves the corresponding chunk from the chunks list, but only if the index is valid (i < len(chunks)) to avoid out-of-range errors.
    return results