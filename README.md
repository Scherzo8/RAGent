# RAG Multi-Agent Assistant

This project is a Retrieval-Augmented Generation (RAG) powered question answering assistant that routes user queries to appropriate tools based on context. It uses a multi-agent setup to intelligently decide between executing mathematical expressions, retrieving definitions via a dictionary API, or querying an LLM for complex, document-grounded answers.

## Architecture

This system uses a modular, multi-agent framework that routes incoming queries to specialized tools based on keyword analysis. It consists of three major subsystems:

- **Tool Agent Layer**: Routes the query to either:
  - A calculator (for arithmetic)
  - A dictionary API (for definitions)
  - A RAG pipeline (for all other queries)
- **RAG Pipeline**:
  - Chunks `.txt` documents
  - Embeds them using Sentence Transformers
  - Stores them in a FAISS index
  - Retrieves relevant chunks to inject into an LLM prompt
- **LLM Wrapper Layer**:
  - Uses either OpenRouter or HuggingFace to complete the answer generation
  - Swap is controlled via a `.env` variable

## Key Design Choices

- **Simple manual agent routing**: Instead of LangChain, routing is done manually for full transparency.
- **Dual LLM backends**: The system supports both OpenRouter and HuggingFace, allowing free use or premium fallback.
- **Readable prompts and logging**: Prompt construction and decision steps are exposed and visible in the UI for debugging and evaluation.
- **Lightweight, testable**: Built without heavy dependencies—fast to run, portable, and transparent.

## Setup Instructions

1. **Install dependencies**:
    ```bash
    poetry install
    ```

2. **Create a `.env` file** in the root directory:
    ```
    LLM_PROVIDER=huggingface  # or "openrouter"
    HUGGINGFACEHUB_API_TOKEN=your_token_here
    OPENROUTER_API_KEY=your_token_here
    ```

3. **Add documents**: Place your `.txt` files in the `data/` folder.

4. **Run ingestion** (only once per dataset change):
    ```bash
    poetry run python core/ingest.py
    ```

5. **Start the app**:
    ```bash
    poetry run python main.py
    ```

## Project Structure

```
ragent/
├── core/
│   ├── agents.py        # Multi-agent routing logic
│   ├── ingest.py        # Chunking + vector indexing
│   ├── retriever.py     # FAISS-based semantic retriever
│   ├── tools.py         # Calculator + dictionary functions
│   └── llm_wrapper.py   # Dual LLM wrapper: OpenRouter + HuggingFace
├── data/                # Input .txt documents
├── index/               # Auto-generated vector index and chunk store
├── ui/
│   └── app.py           # Streamlit UI
├── .env                 # API keys (not committed)
├── .gitignore
├── main.py              # Entrypoint to launch app
├── poetry.lock
└── pyproject.toml
```

## Notes

- The `index/` folder is generated and excluded from version control.
- If using HuggingFace fallback (`flan-t5-base`), responses may be less fluent due to model size limitations.
- Retrieval and chunk injection remain fully functional regardless of LLM provider.

## Demo

To be hosted via Streamlit Cloud or any frontend deployment method. Link can be added here after deployment.
