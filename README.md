# MG Car AI Agent

An AI-powered assistant that helps customers learn about MG Motor cars, get recommendations, pricing information, features, and answers to FAQs.

## Architecture

The system follows a Retrieval-Augmented Generation (RAG) pipeline:

```
Documents → Chunking → Embeddings → Vector DB
                                    ↓
User Query → Embedding → Retrieve → LLM
```

## Features

- **Car Recommendations**: Suggests cars based on user needs (family, budget, features)
- **Pricing Information**: Provides accurate pricing details
- **Feature Details**: Explains car specifications and features
- **FAQ Answers**: Answers common questions about MG cars, booking, service
- **Charging Infrastructure**: Information about MG's EV charging network

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up your Google API key in `.env`:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Run the agent:
   ```bash
   uv run python main.py
   ```

## Data Sources

The agent uses data from the `Data/` folder including:
- Car specifications (JSON)
- FAQs (JSON)
- Booking and service processes (Text)
- Brochures (PDF)
- Support information (JSON)

## Usage

After running `main.py`, you can ask questions like:
- "Recommend a family SUV"
- "What are the features of MG Hector?"
- "How to book an MG car?"
- "Tell me about MG charging stations"

Type 'quit' to exit the interactive mode.

## Technical Details

- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store**: ChromaDB
- **LLM**: Google Gemini 1.5 Pro
- **Chunking**: Recursive character splitter (1000 chars, 200 overlap)