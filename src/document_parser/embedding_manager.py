"""
Sources:
Qdrant homepage - https://qdrant.tech/
OpenAI - https://cookbook.openai.com/examples/vector_databases/qdrant/getting_started_with_qdrant_and_openai
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI, BadRequestError
import os
import pandas as pd
from pathlib import Path
import uuid


class EmbeddingManager:
    def __init__(self) -> None:
        self._init_openai()
        self._init_qdrant()

    def _init_qdrant(self) -> None:
        self._QDRANT_CLIENT = QdrantClient(url="http://localhost:6333")
        self._check_if_collection_exists("default_collection")

    def _init_openai(self):
        if os.getenv("OPENAI_API_KEY") is not None:
            print("OPENAI_API_KEY is ready")
        else:
            print("OPENAI_API_KEY environment variable not found")
        self._OPENAI_CLIENT = OpenAI()
        self._EMBEDDING_MODEL = "text-embedding-3-small"
        if self._EMBEDDING_MODEL == "text-embedding-3-small":
            self._EMBEDDING_SIZE = 1536
        elif self._EMBEDDING_MODEL == "text-embedding-3-large":
            self._EMBEDDING_SIZE = 3072

    def find_embedding(self, query) -> str:

        embedded_query = self._get_embedding(query)

        query_results = client.search(
            collection_name=collection_name,
            query_vector=(vector_name, embedded_query),
            limit=top_k,
        )

        return query_results

    def _get_embedding(self, text):
        try:
            em = (
                self._OPENAI_CLIENT.embeddings.create(
                    input=[text], model=self._EMBEDDING_MODEL
                )
                .data[0]
                .embedding
            )
        except BadRequestError as e:
            print(e)
        return em

    def store_txt_data_from_dir(
        self, dir: str, collection_name: str = "default_collection"
    ):

        dir = Path(dir)
        for pth in dir.iterdir():
            with open(pth, "r") as file:
                text = file.read()
                self._store_single_embedding(text=text, collection_name=collection_name)

    def _check_if_collection_exists(self, collection_name, create_on_missing=True):
        collections = []
        try:
            print("Trying to receive qdrant collections:")
            collections = [
                name[1][0].name for name in self._QDRANT_CLIENT.get_collections()
            ]
        except Exception as e:
            print(e)
            print("Error: Qdrant client could not be reached.")
        print(collections)
        in_collection = not collection_name in collections
        print(in_collection)
        if in_collection and create_on_missing:
            self._QDRANT_CLIENT.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self._EMBEDDING_SIZE, distance=Distance.DOT
                ),
            )

    def _store_single_embedding(self, text: str, collection_name="default_collection"):
        em = self._get_embedding(text=text)
        self._check_if_collection_exists(collection_name)
        self._QDRANT_CLIENT.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    payload={
                        "tag": "red",
                    },
                    vector=em,
                ),
            ],
        )

    def _store_row(self, row):
        pass


if __name__ == "__main__":
    a = EmbeddingManager()
    a.store_txt_data_from_dir(
        "/Users/tobiasgerlach/Documents/Code/document_parser/src/document_parser/batch_chapters/",
        collection_name="chapters",
    )
