from baml_client import b, types

from baml_client.types import Chunk
from pdf_extractor import COLLECTION, CHROMA


class SemanticRAG:
    def __init__(self):
        self.collection = COLLECTION
    def run(self, question: str, depth: int = 2) -> dict[str, str]:
        results = self.collection.query(
            query_texts=[question],
            n_results=depth
        )

        # return results

        chunks = [
            Chunk(document=results['documents'][0][i], distance=results['distances'][0][i])
            for i in range(len(results['documents'][0]))
        ]

        return b.QuestionAnswer(question, chunks)
