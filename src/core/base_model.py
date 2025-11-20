from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any
from loguru import logger


class BaseModel(ABC):
    """
    A professional abstract base class for all OOP entities in Software3-Lab.

    Features:
    ----------
    - Auto-generated UUID for every object
    - Consistent serialization (to_dict)
    - Pretty __repr__
    - Logging hooks
    - LLM integration stub (explain)
    """

    def __init__(self, name: str):
        self.id: str = str(uuid.uuid4())
        self.name: str = name

        logger.debug(f"[BaseModel] Created {self.__class__.__name__} (id={self.id}, name={self.name})")

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert object attributes to a dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"

    # -------------------------------------------------------
    # 🔥 LLM Integration (Llama 2 via llama_client.py)
    # -------------------------------------------------------
    async def explain(self) -> str:
        """
        Uses the LLM client to explain this object in natural language.
        Overridden automatically when llama_client is available.
        """
        try:
            from src.ai.llama_client import llama_explain
            return await llama_explain(self.to_dict())
        except Exception as e:
            logger.error(f"[BaseModel] LLM explanation failed: {e}")
            return "LLM explanation unavailable."
