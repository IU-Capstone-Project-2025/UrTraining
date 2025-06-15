from dataclasses import dataclass
from typing import Optional, Dict, Any
import uuid
import numpy as np


@dataclass
class Document:
    """Document representation with metadata."""

    id: str
    content: str
    vector: Optional[np.ndarray] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid.uuid4())
