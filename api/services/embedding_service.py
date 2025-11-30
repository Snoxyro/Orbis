import os
import requests
from typing import List, Optional
import threading

# Constants
DEFAULT_EMBEDDING_URL = "http://localhost:7860"
DEFAULT_EMBEDDING_DIM = 384  # all-MiniLM-L6-v2
REQUEST_TIMEOUT = 10  # seconds


class EmbeddingService:
    """
    Embedding service client for HuggingFace Text Embeddings Inference (TEI).
    
    Connects to TEI Docker container for generating text embeddings.
    Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
    """
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize embedding service client.
        
        Args:
            api_url: URL of the embedding service (default: http://localhost:7860)
                    Can be overridden via EMBEDDING_SERVICE_URL env variable
        """
        self.api_url = api_url or os.getenv("EMBEDDING_SERVICE_URL", DEFAULT_EMBEDDING_URL)
        self.dimension = DEFAULT_EMBEDDING_DIM
        self._validate_connection()
    
    def _validate_connection(self) -> None:
        """Validate connection to embedding service on initialization."""
        try:
            response = requests.post(
                f"{self.api_url}/embed",
                json={"inputs": "connection test"},
                timeout=5
            )
            response.raise_for_status()
            print(f"✓ Connected to embedding service at {self.api_url}")
            print(f"✓ Model dimension: {self.dimension}")
        except requests.exceptions.Timeout:
            raise ConnectionError(
                f"Timeout connecting to embedding service at {self.api_url}. "
                f"Service may be starting up or not responding."
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to embedding service at {self.api_url}. "
                f"Make sure Docker container is running: docker-compose up -d embeddings"
            )
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(
                f"Embedding service returned error: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            raise ConnectionError(f"Unexpected error connecting to embedding service: {e}")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats (length=384)
            
        Raises:
            RuntimeError: If embedding generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            response = requests.post(
                f"{self.api_url}/embed",
                json={"inputs": text},
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()[0]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate embedding: {e}")
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient than calling embed_text repeatedly).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            ValueError: If texts list is empty
            RuntimeError: If embedding generation fails
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")
        
        try:
            response = requests.post(
                f"{self.api_url}/embed",
                json={"inputs": texts},
                timeout=REQUEST_TIMEOUT * 3  # More time for batch
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate embeddings: {e}")
    
    def get_dimension(self) -> int:
        """Get embedding dimension (384 for all-MiniLM-L6-v2)."""
        return self.dimension


# Thread-safe singleton instance
_embedding_service: Optional[EmbeddingService] = None
_embedding_service_lock = threading.Lock()


def get_embedding_service() -> EmbeddingService:
    """
    Get or create embedding service instance (thread-safe singleton).
    
    Returns:
        Singleton instance of EmbeddingService
    """
    global _embedding_service
    if _embedding_service is None:
        with _embedding_service_lock:
            # Double-check locking pattern
            if _embedding_service is None:
                _embedding_service = EmbeddingService()
    return _embedding_service
