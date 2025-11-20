from __future__ import annotations
from typing import Optional, Dict, Any
from loguru import logger

from src.oop_labs.transport_mode import TransportMode
from src.core.object_registry import ObjectRegistry


class Airplane(TransportMode):
    """
    Base Airplane class (for jets, commercial aircraft, private planes, etc.)

    Features:
    ---------
    - Aviation attributes:
        • wingspan
        • max_altitude
        • num_passengers
    - Flight state machine:
        • takeoff()
        • land()
        • climb()
        • descend()
    - Uses TransportMode for fuel/EV systems and range calculations
    - Safe altitude management + structured telemetry logging
    """

    def __init__(
        self,
        name: str,
        max_speed: float,
        wingspan: Optional[float] = None,
        max_altitude: Optional[float] = None,
        num_passengers: Optional[int] = None,
    ):
        super().__init__(name=name, max_speed=max_speed)

        self.wingspan = wingspan               # feet
        self.max_altitude = max_altitude       # feet
        self.num_passengers = num_passengers

        self.current_altitude = 0
        self.in_air = False

        ObjectRegistry.add(self)

        logger.info(
            f"[Airplane] '{self.name}' created (wingspan={wingspan} ft, "
            f"ceil={max_altitude} ft, pax={num_passengers})"
        )

    # ---------------------------------------------------------
    # Flight Lifecycle
    # ---------------------------------------------------------
    def takeoff(self):
        if self.in_air:
            logger.warning(f"[Airplane] {self.name} is already airborne.")
            return False

        self.in_air = True
        self.current_altitude = 1000  # immediate safe alt
        logger.info(f"[Airplane] {self.name} successfully took off.")
        return True

    def land(self):
        if not self.in_air:
            logger.warning(f"[Airplane] {self.name} is already on the ground.")
            return False

        self.in_air = False
        self.current_altitude = 0
        logger.info(f"[Airplane] {self.name} landed successfully.")
        return True

    # ---------------------------------------------------------
    # Altitude Control
    # ---------------------------------------------------------
    def climb(self, feet: float):
        if not self.in_air:
            logger.error(f"[Airplane] {self.name} cannot climb while on the ground.")
            return False

        new_alt = self.current_altitude + feet

        if self.max_altitude is not None and new_alt > self.max_altitude:
            logger.error(
                f"[Airplane] {self.name} cannot exceed max altitude "
                f"({self.max_altitude} ft). Requested climb to {new_alt} ft."
            )
            return False

        self.current_altitude = new_alt
        logger.info(f"[Airplane] {self.name} climbed to {self.current_altitude} ft.")
        return True

    def descend(self, feet: float):
        if not self.in_air:
            logger.error(f"[Airplane] {self.name} cannot descend while on the ground.")
            return False

        new_alt = self.current_altitude - feet

        if new_alt <= 0:
            logger.info(f"[Airplane] {self.name} descending to runway...")
            return self.land()

        self.current_altitude = new_alt
        logger.info(f"[Airplane] {self.name} descended to {self.current_altitude} ft.")
        return True

    # ---------------------------------------------------------
    # Travel Override (rarely used directly for airplanes)
    # ---------------------------------------------------------
    def travel(self, distance: float) -> bool:
        """
        Airplanes still use range calculations from TransportMode but logs differently.
        """
        logger.info(f"[Airplane] {self.name} preparing to travel {distance} miles.")
        return super().travel(distance)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "wingspan": self.wingspan,
                "max_altitude": self.max_altitude,
                "num_passengers": self.num_passengers,
                "current_altitude": self.current_altitude,
                "in_air": self.in_air,
            }
        )
        return base

    def __str__(self):
        return (
            f"Airplane(name={self.name}, wingspan={self.wingspan}, pax={self.num_passengers}, "
            f"altitude={self.current_altitude}, in_air={self.in_air}, id={self.id})"
        )
