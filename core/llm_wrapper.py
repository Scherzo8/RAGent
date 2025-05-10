import os
from dotenv import load_dotenv


load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter").lower()

if LLM_PROVIDER == "openrouter":

    import openai

    openai.api_key = os.getenv("OPENROUTER_API_KEY")
    openai.api_base = "https://openrouter.ai/api/v1"

elif LLM_PROVIDER == "huggingface":

    from transformers import pipeline

    HF_MODEL = "google/flan-t5-base"
    generator = pipeline(
        "text2text-generation", 
        model=HF_MODEL,
        tokenizer=HF_MODEL,
    )

def construct_prompt(chunks, query):
    context = "\n\n".join(chunks)
    return f"""Answer the question using only the context below.

    Context:
    {context}

    Question: {query}
    Answer:"""  


def query_llm(prompt):

    if LLM_PROVIDER == "openrouter":      
        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response["choices"][0]["message"]["content"].strip()

    elif LLM_PROVIDER == "huggingface":
        response = generator(prompt, max_new_tokens=256)[0]["generated_text"]
        
        return response.strip()

    else:

        return f"LLM provider '{LLM_PROVIDER}' not supported."


def generate_answer(chunks, query):
    prompt = construct_prompt(chunks, query)

    return query_llm(prompt)