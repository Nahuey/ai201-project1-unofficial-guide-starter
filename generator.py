from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

def generate_response(query,retrieved_chunks):

    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )
    

    print(len(retrieved_chunks))

    context_texts = []
    sources = set()

    for chunk in retrieved_chunks:
        text = chunk.get("text", "")
        # Fallback to "Unknown Source" if metadata is missing
        title = chunk.get("metadata", {}).get("title", "Unknown Source")
        
        context_texts.append(f"--- Document: {title} ---\n{text}")
        sources.add(title)

    joined_context = "\n\n".join(context_texts)

    # 2. Build the strict System Prompt
    system_prompt = f"""
    You are a precise answering assistant. Your strict requirement is to answer the user's question using ONLY the information provided in the context below.
    
    CRITICAL RULES:
    1. Base your answer entirely on the provided context. Do NOT use outside knowledge or training data.
    2. You MUST embed inline source citations directly into your sentences where the facts are stated. Use the format: [Source: Document Title].
    3. If the context does not contain enough information to fully answer the question, you must respond EXACTLY with: "I don't have enough information on that." Do not attempt to guess.
    4. Keep your answer clear, concise, and direct. Do not add conversational filler.
    
    CONTEXT:
    {joined_context}
    """

    try:
        # 3. Call the Groq API
        response = _client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            model=LLM_MODEL,
            temperature=0, # Force deterministic, fact-based output
        )
        
        llm_answer = response.choices[0].message.content.strip()

        # 4. Check for the missing info fallback
        if "I don't have enough information on that." in llm_answer:
            return llm_answer, "None"
        
        # 5. Programmatically append the sources
        source_list = "\n".join([f"- {source}" for source in sorted(sources)])
        
        return llm_answer, source_list

    except Exception as e:
        return f"An error occurred during generation: {e}"