from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EmbeddingEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # This will download the model on the first run
        self.model = SentenceTransformer(model_name)
    
    def get_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)
        
    def get_embeddings(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts)
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.get_embedding(text1).reshape(1, -1)
        emb2 = self.get_embedding(text2).reshape(1, -1)
        sim = cosine_similarity(emb1, emb2)[0][0]
        return float(sim)

# Singleton instance
embedding_engine = EmbeddingEngine()
