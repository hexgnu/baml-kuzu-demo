from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer
import fitz
import chromadb
from chromadb.config import Settings


CHUNK_SIZE=120
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

CHROMA_DIR = './chroma_db'

CHROMA = chromadb.PersistentClient(path=CHROMA_DIR)

COLLECTION_NAME = 'drug_interactions'

COLLECTION = CHROMA.get_or_create_collection(name=COLLECTION_NAME)


def create_markdown(filename: Path) -> Path:
    doc = fitz.open(filename)

    text = ""

    for page in doc:
        text += page.get_text()

    output_dir = Path('../data/extracted_data')

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename.with_suffix('.md').name

    with output_path.open("w") as f:
        f.write(text)

    return output_path


def chunk_text(text: str, chunk_size=CHUNK_SIZE) -> List[str]:
    return [
        text[i:i+chunk_size] for i in range(0, len(text), chunk_size)
    ]

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    return model.encode(chunks, normalize_embeddings=True).tolist()


def save_chroma(chunks: List[str], client=CHROMA, collection=COLLECTION) -> bool:
    # embeddings = embed_chunks(chunks)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    return collection.upsert(documents=chunks, ids=ids)


if __name__ == '__main__':
    output_path = create_markdown(
        Path('../data/pdf/Medication_Side_Effect_Flyer.pdf')
    )

    print(f"Results written to {output_path}")

    with output_path.open("r") as f:
        chunks = chunk_text(f.read())

        save_chroma(chunks)

    # pymupdf
    # chunk up using minilm
    # then chunk up into a chroma db
    # store locally
