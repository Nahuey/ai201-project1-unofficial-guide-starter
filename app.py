from ingest import load_documents, recursive_chunk_document, semantic_chunk_document
from retriever import embed_and_store, retrieve, get_collection
import gradio as gr
from generator import generate_response

def run_ingestion():
    """
    Load rule documents, chunk them, and store in ChromaDB.

    If the vector store is already populated, ingestion is skipped.
    To re-ingest (e.g. after changing your chunking strategy), delete the
    ./chroma_db folder and restart the app.
    """
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Ingesting documents...")
    documents = load_documents()
    all_chunks = []

    # Documents that require structural logic to keep headers and bullet points together
    structured_docs = [
        "10 Best Spots To Study On Campus",
        "10 Spaces To Find Serenity On Campus",
        "15 Ideas For Your Ucsd Bucket List",
        "26 Things To Do In Sd",
        "Best Beaches In Sd",
        "Best Boba In Sd"
    ]

    for doc in documents:
        title = doc["title"]
        text = doc["text"]

        if title in structured_docs:
            print(f"--> Routing '{title}' to Structural Chunker...")
            chunks = semantic_chunk_document(text, title)
        else:
            print(f"--> Routing '{title}' to Recursive Chunker...")
            chunks = recursive_chunk_document(text, title)
            
        all_chunks.extend(chunks)

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {len(all_chunks)} chunks stored.")
    else:
        print(
            "\n⚠️  No chunks produced. Make sure chunk_document() is implemented in ingest.py.\n"
        )


def handle_query(query):
    if not query.strip():
        return ""
    retrieved = retrieve(query)
    answer, sources = generate_response(query, retrieved)
    return answer, sources

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Unofficial Guide — starting up")
    print("="*50 + "\n")
    run_ingestion()
    demo.launch()