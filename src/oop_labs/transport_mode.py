from __future__ import annotations
from typing import Optional, Dict, Any
from loguru import logger

from src.core.base_model import BaseModel
from src.core.object_registry import ObjectRegistry


class TransportMode(BaseModel):
    """
    Base class for transportation modes (cars, motorcycles, boats, airplanes, etc.)

    Provides:
    ---------
    - Common attributes (name, max_speed)
    - Optional fuel system for subclasses
    - Range estimation
    - Structured logging
    - LLM/MCP explain() support via BaseModel
    """

    def __init__(self, name: str, max_speed: float):
        super().__init__(name=name)
        self.max_speed = max_speed  # mph
        self.fuel_capacity: Optional[float] = None  # gallons (optional)
        self.current_fuel: Optional[float] = None   # gallons (optional)
        self.mpg: Optional[float] = None            # miles per gallon (optional)

        ObjectRegistry.add(self)

        logger.debug(
            f"[TransportMode] Created {self.name} "
            f"with max_speed={self.max_speed} mph"
        )

    # ---------------------------------------------------------
    # Fuel system (optional for subclasses)
    # ---------------------------------------------------------
    def configure_fuel_system(self, mpg: float, fuel_capacity: float):
        """Enable and initialize a fuel system for this transport mode."""
        self.mpg = mpg
        self.fuel_capacity = fuel_capacity
        self.current_fuel = 0.0

        logger.info(
            f"[TransportMode] {self.name} fuel system configured: "
            f"mpg={mpg}, capacity={fuel_capacity} gal"
        )

    def add_fuel(self, gallons: float):
        """Add fuel to the vehicle, respecting the capacity."""
        if self.current_fuel is None:
            raise RuntimeError("Fuel system not configured for this vehicle.")

        if gallons <= 0:
            logger.warning("[TransportMode] Cannot add non-positive fuel amount.")
            return

        new_level = min(self.fuel_capacity, self.current_fuel + gallons)
        logger.info(
            f"[TransportMode] Adding {gallons} gal to {self.name}. "
            f"Fuel: {self.current_fuel} -> {new_level}"
        )

        self.current_fuel = new_level

    def estimate_range(self) -> Optional[float]:
        """Return estimated remaining range in miles based on fuel and mpg."""
        if self.current_fuel is None or self.mpg is None:
            return None
        return self.current_fuel * self.mpg

    # ---------------------------------------------------------
    # Travel Simulation
    # ---------------------------------------------------------
    def travel(self, distance: float) -> bool:
        """
        Simulate traveling a distance. Returns True if successful.
        Vehicles without fuel systems always succeed.
        """
        if distance <= 0:
            logger.warning("[TransportMode] Travel distance must be positive.")
            return False

        # If no fuel system = treat as always successful (e.g., bikes/boats/EVs)
        if self.mpg is None:
            logger.info(
                f"[TransportMode] {self.name} traveled {distance} miles "
                "(no fuel system)."
            )
            return True

        required_fuel = distance / self.mpg

        if self.current_fuel < required_fuel:
            logger.warning(
                f"[TransportMode] {self.name} cannot travel {distance} miles. "
                f"Required={required_fuel:.2f} gal, Available={self.current_fuel:.2f} gal"
            )
            return False

        self.current_fuel -= required_fuel

        logger.info(
            f"[TransportMode] {self.name} traveled {distance} miles. "
            f"Fuel remaining={self.current_fuel:.2f} gal"
        )
        return True

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "max_speed": self.max_speed,
                "mpg": self.mpg,
                "fuel_capacity": self.fuel_capacity,
                "current_fuel": self.current_fuel,
                "estimated_range": self.estimate_range(),
            }
        )
        return base

    def __str__(self):
        return (
            f"TransportMode(name={self.name}, max_speed={self.max_speed}, "
            f"fuel={self.current_fuel}/{self.fuel_capacity}, mpg={self.mpg}, id={self.id})"
        )

