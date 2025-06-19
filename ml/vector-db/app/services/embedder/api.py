import time
import logging
import requests
from typing import List, Union, Optional, Dict
from abc import abstractmethod

import numpy as np

from .base import BaseEmbedder


logger = logging.getLogger(__name__)


class APIEmbedder(BaseEmbedder):
    """API-based embedder that calls external embedding services."""

    def __init__(
        self,
        api_url: str,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        dimension: int = 1536,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize API embedder.

        Args:
            api_url: The API endpoint URL for embeddings
            api_key: API key for authentication
            model_name: Model name to use for embeddings (if required by API)
            dimension: Embedding dimension
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            timeout: Request timeout in seconds
            headers: Additional headers to send with requests
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self._dimension = dimension
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

        self.headers = headers or {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.headers.setdefault("Content-Type", "application/json")

    def encode(
        self, texts: Union[str, List[str]], batch_size: int = 1, **kwargs
    ) -> np.ndarray:
        """
        Encode texts into embeddings using API calls.

        Args:
            texts: Text or list of texts to encode
            batch_size: Number of texts to send in each API request
            **kwargs: Additional arguments passed to the API

        Returns:
            numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]

        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            embeddings = self._call_api(batch_texts, **kwargs)
            all_embeddings.extend(embeddings)

        return np.array(all_embeddings)

    @abstractmethod
    def _call_api(self, texts: List[str], **kwargs) -> List[List[float]]:
        """
        Make API call to get embeddings for the given texts.
        """
        pass

    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self._dimension


class KlusterAIEmbedder(APIEmbedder):
    """KlusterAI API embedder with predefined settings."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "BAAI/bge-m3",
        dimension: int = 1024,
        **kwargs,
    ):
        """
        Initialize KlusterAI embedder.

        Args:
            api_key: API key
            model_name: model name
            dimension: Embedding dimension
            **kwargs: Additional arguments passed to APIEmbedder
        """
        super().__init__(
            api_url="https://api.kluster.ai/v1/embeddings",
            api_key=api_key,
            model_name=model_name,
            dimension=dimension,
            **kwargs,
        )

    def _call_api(self, texts: List[str], **kwargs) -> List[List[float]]:
        """
        Make API call to KlusterAI embeddings endpoint.

        Args:
            texts: List of texts to embed
            **kwargs: Additional arguments for the API

        Returns:
            List of embedding vectors
        """
        payload = {"input": texts, "model": self.model_name}

        payload.update(kwargs)

        for attempt in range(self.max_retries + 1):
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()

                result = response.json()

                # Handle OpenAI-style response format
                if "data" in result:
                    return [item["embedding"] for item in result["data"]]
                elif "embeddings" in result:
                    return result["embeddings"]
                elif isinstance(result, list):
                    return result
                else:
                    raise ValueError(f"Unexpected API response format: {result}")

            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"KlusterAI API request failed (attempt {attempt + 1}): {e}"
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2**attempt))
                else:
                    raise Exception(
                        f"KlusterAI API request failed after {self.max_retries + 1} attempts: {e}"
                    )
            except Exception as e:
                logger.error(f"Unexpected error during KlusterAI API call: {e}")
                raise


if __name__ == "__main__":
    import os
    import dotenv

    dotenv.load_dotenv()

    api_key = os.getenv("KLUSTER_AI_API_KEY")
    if not api_key:
        print("Please set KLUSTER_AI_API_KEY environment variable")
        exit(1)

    embedder = KlusterAIEmbedder(api_key=api_key)

    test_texts = [
        "This is a test sentence.",
        "Another example text for embedding.",
        "Machine learning is fascinating.",
    ]

    try:
        embeddings = embedder.encode(test_texts, 1)
        print(f"Generated embeddings shape: {embeddings.shape}")
        print(f"Embedding dimension: {embedder.get_dimension()}")
        print("KlusterAI embedder test successful!")
    except Exception as e:
        print(f"Test failed: {e}")
