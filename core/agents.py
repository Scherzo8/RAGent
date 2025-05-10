from core.retriever import get_relevant_chunks
from core.llm_wrapper import generate_answer
from core.tools import calculate_expression, define_word


def route_query(query: str):

    lowered = query.lower()

    if any(keyword in lowered for keyword in ["calculate", "solve", "+", "-", "*", "/", "%"]):
        decision = "Tool: calculator"

        result = calculate_expression(query)

    elif any(keyword in lowered for keyword in ["define", "meaning of", "what is", "explain"]):
        last_word = query.split()[-1]
        decision = f"Tool: dictionary (word: {last_word})"
        result = define_word(last_word)
        
    else:
        decision = "Tool: LLM (RAG)"
        chunks = get_relevant_chunks(query)
        result = generate_answer(chunks, query)

    return decision, result