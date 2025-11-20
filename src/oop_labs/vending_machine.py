from __future__ import annotations
from typing import Dict, Any
from loguru import logger

from src.core.base_model import BaseModel
from src.core.object_registry import ObjectRegistry


class VendingMachine(BaseModel):
    """
    A professional vending machine model with inventory tracking,
    purchasing logic, restocking, and LLM explanation support.

    Demonstrates:
    -------------
    - Clean OOP
    - State management
    - Inventory operations
    - Logging for observability
    - AI hooks via BaseModel.explain()
    """

    def __init__(self, name: str, initial_inventory: int = 0):
        super().__init__(name=name)
        self.inventory = initial_inventory

        ObjectRegistry.add(self)
        logger.debug(f"[VendingMachine] Created with inventory={self.inventory}")

    # ---------------------------------------------------------
    # Core Behavior
    # ---------------------------------------------------------
    def purchase(self, quantity: int) -> bool:
        """
        Attempt to purchase a number of items.
        Returns True if successful, False otherwise.
        """
        if quantity <= 0:
            logger.warning("[VendingMachine] Cannot purchase non-positive quantity.")
            return False

        if self.inventory < quantity:
            logger.warning(
                f"[VendingMachine] Purchase failed. "
                f"Requested={quantity}, Available={self.inventory}"
            )
            return False

        self.inventory -= quantity
        logger.info(f"[VendingMachine] Purchased {quantity}. Remaining={self.inventory}")
        return True

    def restock(self, quantity: int) -> None:
        """Add items to the machine inventory."""
        if quantity <= 0:
            logger.warning("[VendingMachine] Cannot restock with non-positive quantity.")
            return

        self.inventory += quantity
        logger.info(f"[VendingMachine] Restocked {quantity}. Total={self.inventory}")

    # ---------------------------------------------------------
    # Serialization & Representation
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({"inventory": self.inventory})
        return base

    def __str__(self) -> str:
        return (
            f"VendingMachine(name={self.name}, inventory={self.inventory}, id={self.id})"
        )
