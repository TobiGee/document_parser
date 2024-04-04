"""
Sources:
Qdrant homepage - https://qdrant.tech/
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class EmbeddingManager:
    def __init__(self) -> None:
        self._init_qdrant()

    def _init_qdrant(self) -> None:
        self._QDRANT_CLIENT = QdrantClient(url="http://localhost:6333")
        self._QDRANT_CLIENT.create_collection(
            collection_name="test_collection",
            vectors_config=VectorParams(size=4, distance=Distance.DOT),
        )

    def find_embedding(self) -> str:
        pass


if __name__ == "__main__":
    a = EmbeddingManager()
