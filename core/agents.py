from core.retriever import get_relevant_chunks
from core.llm_wrapper import generate_answer
from core.tools import calculate_expression, define_word


def route_query(query: str):

    lowered = query.lower()

    if any(keyword in lowered for keyword in ["calculate", "solve", "+", "-", "*", "/", "%"]):
        print("Routing to calculator...")

        return "Tool: calculator", calculate_expression(query)
    
    elif any(keyword in lowered for keyword in ["define", "meaning of", "what is", "explain"]):
        last_word = query.split()[-1]
        print(f"Routing to dictionary (word: {last_word})...")

        return "Tool: dictionary", define_word(last_word)
    
    else:
        print("Routing to RAG + LLM...")
        chunks = get_relevant_chunks(query)
        answer = generate_answer(chunks, query)
        
        return "Tool: LLM (RAG)", answer