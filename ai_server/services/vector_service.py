from qdrant_client import QdrantClient


class VectorService:

    def __init__(self):

        self.client = None

        try:
            self.client = QdrantClient(
                url="http://localhost:6333"
            )
        except:
            pass

    def store_memory(self, payload):
        return True


vector_service = VectorService()
