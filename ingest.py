import os
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import DOCS_PATH

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents():
    """Load all .txt rule documents from the docs folder."""
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            title = filename.replace(".txt", "").replace("-", " ").title()
            documents.append({
                "title": title,
                "filename": filename,
                "text": text
            })
    print(f"Loaded {len(documents)} rule document(s): {[d['title'] for d in documents]}")
    return documents

def recursive_chunk_document(text, title):
    chunk_size = 1000
    overlap = 150
    prefix = title.lower().replace(" ","_")
    separators = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    chunks = []

    def split_text(text_split, current_separators):
        if not current_separators:
            return [text_split]
        
        curr_sep = current_separators[0]
        remaining_separators = current_separators[1:]

        if curr_sep == "":
            return [
                text_split[i:i + chunk_size] 
                for i in range(0, len(text_split), chunk_size - overlap)
            ]
    
        splits = text_split.split(curr_sep)
        good_splits = []
        current_accumulation = []
        curr_length = 0

        for split in splits:
            split_len = len(split)

            # 1. Finalize the chunk if adding this split pushes it over the limit
            if curr_length + split_len + len(curr_sep) > chunk_size and current_accumulation:
                chunk_text = curr_sep.join(current_accumulation)
                good_splits.append(chunk_text)
                
                # Setup the overlap for the next chunk
                overlap_text = chunk_text[-overlap:] if overlap > 0 else ""
                current_accumulation = [overlap_text] if overlap_text else []
                curr_length = len(current_accumulation[0]) if current_accumulation else 0

            # 2. Check if the current single split is STILL larger than chunk_size
            if split_len > chunk_size:
                # Flush the current accumulation before recursing
                if current_accumulation:
                    good_splits.append(curr_sep.join(current_accumulation))
                    current_accumulation = []
                    curr_length = 0
                
                # Recurse using the remaining separators
                sub_splits = split_text(split, remaining_separators)
                good_splits.extend(sub_splits)
            else:
                # 3. Standard case: add the split to the current block
                current_accumulation.append(split)
                curr_length += split_len + len(curr_sep)

        # 4. Catch any leftover text after the loop
        if current_accumulation:
            good_splits.append(curr_sep.join(current_accumulation))

        return [s for s in good_splits if s.strip()]

    # --- Execute the splitting logic ---
    raw_text_chunks = split_text(text, separators)

    # --- Format into the requested dictionaries ---
    for index, chunk_text in enumerate(raw_text_chunks):
        if chunk_text.strip():
            chunks.append({
                "text": chunk_text.strip(),
                "title": title,
                "chunk_id": f"{prefix}_{index}"
            })

    return chunks

def semantic_chunk_document(text, title, similarity_threshold=0.3):
    """
    Chunks a document by grouping sentences/lines based on their semantic similarity.
    Perfect for listicles and markdown files where bullet points belong to a specific header.
    """
    prefix = title.lower().replace(" ", "_")
    chunks = []
    
    # 2. Split by newlines (keeps bullet points and headers intact better than splitting by periods)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return chunks

    # 3. Generate embeddings for every line in the document
    embeddings = embed_model.encode(lines)
    
    raw_chunks = []
    current_chunk = [lines[0]]
    
    # 4. Compare consecutive lines to see if they belong to the same topic
    for i in range(1, len(lines)):
        # Calculate how similar this line is to the previous line
        sim = cosine_similarity(
            [embeddings[i]], 
            [embeddings[i-1]]
        )[0][0]
        
        # If the lines are semantically related (above threshold), keep them together
        if sim >= similarity_threshold:
            current_chunk.append(lines[i])
        else:
            # Topic shifted: save the current chunk and start a fresh one
            raw_chunks.append("\n".join(current_chunk))
            current_chunk = [lines[i]]
            
    # Catch the final chunk after the loop finishes
    if current_chunk:
        raw_chunks.append("\n".join(current_chunk))
        
    # 5. Package into the exact dictionary format used in recursive_chunk_document
    for index, chunk_text in enumerate(raw_chunks):
        if chunk_text.strip():
            chunks.append({
                "text": chunk_text.strip(),
                "title": title,
                # Added '_sem_' to the ID so you know which chunker generated it
                "chunk_id": f"{prefix}_sem_{index}" 
            })
            
    return chunks

# if __name__=="__main__":
#     main()