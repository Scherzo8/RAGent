import os
from dotenv import load_dotenv
import openai


load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"


def construct_prompt(chunks, query):

    context = "\n\n".join(chunks)

    return f"""Use the following context to answer the user's question as clearly and accurately as possible.

    Context:
    {context}

    Question: {query}
    Answer:"""


def query_llm(prompt):

    print("Querying Openrouter llm")

    response = openai.ChatCompletion.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response["choices"][0]["message"]["content"].strip()


def generate_answer(chunks, query):
    prompt = construct_prompt(chunks, query)
    return query_llm(prompt)