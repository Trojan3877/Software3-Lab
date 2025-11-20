from __future__ import annotations
from typing import Dict, Optional, Type
from loguru import logger
from src.core.base_model import BaseModel


class ObjectRegistry:
    """
    Global registry for all OOP objects in Software3-Lab.

    Purpose:
    --------
    - Store references to all created objects
    - Enable lookup by ID
    - Allow MCP tools & AI systems to interact with live objects
    - Enable cross-object simulation
    """

    _registry: Dict[str, BaseModel] = {}

    @classmethod
    def add(cls, obj: BaseModel) -> None:
        cls._registry[obj.id] = obj
        logger.debug(f"[ObjectRegistry] Registered {obj.__class__.__name__} (id={obj.id})")

    @classmethod
    def get(cls, object_id: str) -> Optional[BaseModel]:
        obj = cls._registry.get(object_id)
        if obj:
            logger.debug(f"[ObjectRegistry] Retrieved {obj}")
        else:
            logger.warning(f"[ObjectRegistry] Object with id={object_id} not found.")
        return obj

    @classmethod
    def all(cls) -> Dict[str, BaseModel]:
        return cls._registry.copy()

    @classmethod
    def remove(cls, object_id: str) -> bool:
        if object_id in cls._registry:
            removed = cls._registry.pop(object_id)
            logger.debug(f"[ObjectRegistry] Removed {removed}")
            return True
        logger.warning(f"[ObjectRegistry] Cannot remove: id={object_id} not found.")
        return False

    @classmethod
    def clear(cls) -> None:
        logger.debug("[ObjectRegistry] Cleared all objects.")
        cls._registry.clear()
