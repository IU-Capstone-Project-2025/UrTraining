from typing import Literal

import torch


def pool_embeddings(
    token_embeddings: torch.Tensor,
    attention_mask: torch.Tensor,
    strategy: Literal["mean", "cls", "max"] = "mean",
) -> torch.Tensor:
    """
    Apply pooling strategy to token embeddings.

    Args:
        token_embeddings: Token embeddings [batch_size, seq_len, hidden_size]
        attention_mask: Attention mask [batch_size, seq_len]
        strategy: Pooling strategy

    Returns:
        Pooled embeddings [batch_size, hidden_size]
    """
    if strategy == "mean":
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    elif strategy == "cls":
        return token_embeddings[:, 0]

    elif strategy == "max":
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        token_embeddings[input_mask_expanded == 0] = -1e9
        return torch.max(token_embeddings, 1)[0]

    else:
        raise ValueError(f"Unknown pooling strategy: {strategy}")
