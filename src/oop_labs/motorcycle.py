from __future__ import annotations
from typing import Optional, Dict, Any
from loguru import logger

from src.oop_labs.motor_vehicle import MotorVehicle
from src.core.object_registry import ObjectRegistry


class Motorcycle(MotorVehicle):
    """
    Motorcycle class - extends MotorVehicle

    Features:
    ---------
    - Motorcycle-specific attributes:
        • seat_height
        • is_offroad_capable
        • has_abs
    - Unique motorcycle actions:
        • wheelie()
        • lean_angle safety checks
    - Fully integrated with MotorVehicle (fuel or EV system)
    - Structured logging for telemetry and debugging
    """

    def __init__(
        self,
        name: str,
        max_speed: float,
        horsepower: int,
        weight_lbs: float,
        seat_height: Optional[float] = None,
        is_offroad_capable: bool = False,
        has_abs: bool = True,
    ):
        super().__init__(
            name=name,
            max_speed=max_speed,
            horsepower=horsepower,
            weight_lbs=weight_lbs,
        )

        self.seat_height = seat_height
        self.is_offroad_capable = is_offroad_capable
        self.has_abs = has_abs

        ObjectRegistry.add(self)

        logger.info(
            f"[Motorcycle] Created motorcycle '{self.name}' "
            f"(hp={horsepower}, weight={weight_lbs}, offroad={is_offroad_capable}, abs={has_abs})"
        )

    # ---------------------------------------------------------
    # Motorcycle-specific Actions
    # ---------------------------------------------------------
    def wheelie(self):
        """Perform a wheelie — purely simulated."""
        logger.warning(f"[Motorcycle] {self.name} attempted a wheelie! 🤘🏽")
        return f"{self.name} lifts the front wheel briefly — dangerous but impressive!"

    def lean(self, angle: float):
        """
        Simulate motorcycle leaning.
        If lean angle > 50 degrees, consider unsafe.
        """
        if angle <= 0:
            return "Lean angle must be positive."

        if angle > 50:
            logger.error(
                f"[Motorcycle] {self.name} leaned dangerously at {angle}° — unsafe!"
            )
            return f"{self.name} leans too far! {angle}° is unsafe!"
        else:
            logger.info(
                f"[Motorcycle] {self.name} leans safely at {angle}°."
            )
            return f"{self.name} leans smoothly at {angle}°."

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "seat_height": self.seat_height,
                "is_offroad_capable": self.is_offroad_capable,
                "has_abs": self.has_abs,
            }
        )
        return base

    def __str__(self):
        return (
            f"Motorcycle(name={self.name}, hp={self.horsepower}, weight={self.weight_lbs}, "
            f"seat_height={self.seat_height}, offroad={self.is_offroad_capable}, "
            f"abs={self.has_abs}, id={self.id})"
        )
