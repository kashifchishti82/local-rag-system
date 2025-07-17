import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple

class FaissVectorStore:
    """A vector store that uses FAISS for indexing and a separate file for metadata."""

    def __init__(self, index_path: str = "./data/vector_store.faiss", metadata_path: str = "./data/metadata.pkl"):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index: faiss.Index | None = None
        self.metadata: Dict[int, Dict[str, Any]] = {}

        # Ensure the data directory exists
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.load()

    def add(self, chunks: List[str], embeddings: np.ndarray, metadatas: List[Dict[str, Any]]):
        """Adds chunks, their embeddings, and metadata to the store."""
        if self.index is None:
            dimension = embeddings.shape[1]
            # Using IndexFlatL2 for simplicity, good for exact search.
            self.index = faiss.IndexFlatL2(dimension)

        if embeddings.shape[0] != len(chunks) or len(chunks) != len(metadatas):
            raise ValueError("The number of chunks, embeddings, and metadatas must be the same.")

        start_index = self.index.ntotal
        self.index.add(embeddings.astype('float32'))

        for i, (chunk, metadata) in enumerate(zip(chunks, metadatas)):
            doc_id = start_index + i
            self.metadata[doc_id] = {
                "chunk_text": chunk,
                **metadata,
            }

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Searches the vector store for the most similar chunks."""
        if self.index is None or self.index.ntotal == 0:
            return []

        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, doc_id in enumerate(indices[0]):
            if doc_id != -1: # FAISS returns -1 for no result
                score = distances[0][i]
                results.append((self.metadata[doc_id], score))
        return results

    def save(self):
        """Saves the FAISS index and metadata to disk."""
        if self.index:
            faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """Loads the FAISS index and metadata from disk."""
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        if self.metadata_path.exists():
            with self.metadata_path.open("rb") as f:
                self.metadata = pickle.load(f)
