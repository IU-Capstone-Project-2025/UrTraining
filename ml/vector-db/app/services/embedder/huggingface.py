import torch
import numpy as np
from typing import List, Union, Optional
from transformers import AutoModel, AutoTokenizer

from .base import BaseEmbedder
from .pooling import pool_embeddings


class HuggingFaceEmbedder(BaseEmbedder):
    """Hugging Face transformer-based embedder."""

    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        max_length: int = 512,
        pooling_strategy: str = "mean",
        normalize: bool = True,
    ):
        self.model_name: str = model_name
        self.max_length: int = max_length
        self.pooling_strategy: str = pooling_strategy
        self.normalize: bool = normalize

        self.device: str = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        self._dimension = self.model.config.hidden_size

    def encode(
        self, texts: Union[str, List[str]], batch_size: int = 32, **kwargs
    ) -> np.ndarray:
        """Encode texts into embeddings."""
        if isinstance(texts, str):
            texts = [texts]

        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            # Tokenize
            encoded = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt",
            )
            encoded = {k: v.to(self.device) for k, v in encoded.items()}

            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**encoded)
                embeddings = pool_embeddings(
                    outputs.last_hidden_state,
                    encoded["attention_mask"],
                    self.pooling_strategy,
                )

                if self.normalize:
                    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

                all_embeddings.append(embeddings.cpu().numpy())

        return np.vstack(all_embeddings)

    def get_dimension(self) -> int:
        return self._dimension
