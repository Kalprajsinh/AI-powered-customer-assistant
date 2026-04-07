## Architecture

The system follows a Retrieval-Augmented Generation (RAG) pipeline:

```
Documents -> Load/Transform -> Chunking -> Embeddings -> FAISS Vector Store
                              ↑
                        Redis Chat History
                              ↑
User Query -> Retrieval -> LLM -> Answer
```
## 📸 Project Screenshots

<p align="center">
  <img src="image\1.png" width="45%" />
  <img src="image\2.png" width="45%" />
</p>

<p align="center">
  <img src="image\3.png" width="45%" />
  <img src="image\4.png" width="45%" />
</p>

## Features

- **Car Recommendations**: Suggests cars based on user needs (family, budget, features)
- **Pricing Information**: Provides accurate pricing details
- **Feature Details**: Explains car specifications and features
- **FAQ Answers**: Answers common questions about MG cars, booking, service
- **Charging Infrastructure**: Information about MG's EV charging network

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
- **Vector Store**: FAISS
- **LLM**: Google Gemini 1.5 Pro
- **Chunking**: Recursive character splitter (1000 chars, 200 overlap)