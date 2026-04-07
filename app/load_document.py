
from langchain_core.documents import Document
import json
from pathlib import Path
from pypdf import PdfReader


def load_documents(data_folder: str) -> list[Document]:
    documents = []
    data_path = Path(data_folder)

    for file_path in data_path.rglob('*'):
        if file_path.is_file():
            try:
                if file_path.suffix.lower() == '.txt':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append(Document(
                            page_content=content,
                            metadata={"source": str(file_path), "type": "text"}
                        ))
                elif file_path.suffix.lower() == '.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                        
                            for item in data:
                                content = f"Question: {item.get('question', '')}\nAnswer: {item.get('answer', '')}"
                                documents.append(Document(
                                    page_content=content,
                                    metadata={"source": str(file_path), "type": "faq"}
                                ))
                        else:
                          
                            content = json.dumps(data, indent=2)
                            documents.append(Document(
                                page_content=content,
                                metadata={"source": str(file_path), "type": "json"}
                            ))
                elif file_path.suffix.lower() == '.pdf':
                    reader = PdfReader(file_path)
                    content = ""
                    for page in reader.pages:
                        content += page.extract_text() + "\n"
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": str(file_path), "type": "pdf"}
                    ))
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    return documents