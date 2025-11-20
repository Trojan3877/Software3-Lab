from __future__ import annotations
from typing import Dict, Any
from loguru import logger

from src.core.base_model import BaseModel
from src.core.object_registry import ObjectRegistry


class Pet(BaseModel):
    """
    Represents a Pet with a name, age, and optional species.

    This class demonstrates clean OOP design using:
    - Inheritance from BaseModel
    - Serialization
    - MCP-ready object behavior
    - LLM explanation support via BaseModel.explain()
    """

    def __init__(self, name: str, age: int, species: str = "Unknown"):
        super().__init__(name=name)
        self.age = age
        self.species = species

        ObjectRegistry.add(self)
        logger.debug(f"[Pet] Created Pet(name={name}, age={age}, species={species})")

    # -----------------------------------
    # Core OOP functionality
    # -----------------------------------
    def birthday(self) -> None:
        """Increment the pet's age by 1 year."""
        self.age += 1
        logger.info(f"[Pet] {self.name} just turned {self.age} years old!")

    # -----------------------------------
    # Serialization
    # -----------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Pet into a dictionary."""
        base = super().to_dict()
        base.update(
            {
                "age": self.age,
                "species": self.species,
            }
        )
        return base

    # -----------------------------------
    # Representation
    # -----------------------------------
    def __str__(self) -> str:
        return f"Pet(name={self.name}, age={self.age}, species={self.species}, id={self.id})"
