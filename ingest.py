import os
from config import DOCS_PATH

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

def chunk_document(text,title):
    chunk_size = 1000
    overlap = 150


def main():
    load_documents()

# Using the special variable 
# __name__
if __name__=="__main__":
    main()