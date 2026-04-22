def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]: # This function takes a string of text and splits it into smaller chunks of a specified size, with an optional overlap between chunks to maintain context. It returns a list of text chunks.
    if not text: 
        return []
    
    chunks = [] # Initialize an empty list to hold the chunks of text
    start = 0 # Start index for slicing the text
    
    while start < len(text):
        end = start + chunk_size # Calculate the end index for the current chunk based on the specified chunk size
        chunk = text[start: end] # Slice the text from the start index to the end index to create a chunk
        
        if chunk.strip(): # Check if the chunk is not just whitespace before adding it to the list of chunks
            chunks.append(chunk.strip()) # Add the chunk to the list, stripping any leading or trailing whitespace
            
        start += chunk_size - overlap # Move the start index forward by the chunk size minus the overlap to create the next chunk, allowing for some overlap between chunks to maintain context
        
    return chunks