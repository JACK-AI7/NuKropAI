from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import logging
from .config import config

logger = logging.getLogger(__name__)

class QdrantMemory:
    def __init__(self):
        self.client = QdrantClient(config.QDRANT_HOST)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.collection_name = "agri_memory"
        self._init_collection()

    def _init_collection(self):
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            logger.info("✅ Qdrant Collection Initialized")
        except Exception as e:
            logger.error(f"❌ Qdrant Init Failed: {e}")

    def search(self, query, limit=3):
        vector = self.model.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit
        )
        return [{"score": r.score, "payload": r.payload} for r in results]

    def add_memory(self, text, metadata):
        vector = self.model.encode(text).tolist()
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=abs(hash(text)), vector=vector, payload=metadata)]
        )

qdrant_memory = QdrantMemory()
