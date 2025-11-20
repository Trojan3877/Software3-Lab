from __future__ import annotations
from typing import Optional, Dict, Any
from loguru import logger

from src.oop_labs.airplane import Airplane
from src.core.object_registry import ObjectRegistry


class JetPlane(Airplane):
    """
    Advanced Jet Plane class.

    Adds:
    -----
    • supersonic mode (Mach 1+)
    • afterburner simulation
    • barrel roll maneuver
    • immelmann turn
    • auto-pilot state machine
    • military/aerobatics-grade safety checks
    """

    SPEED_OF_SOUND_MPH = 767  # Mach 1

    def __init__(
        self,
        name: str,
        max_speed: float,
        wingspan: float,
        max_altitude: float,
        num_passengers: int = 1,
        is_military: bool = False,
    ):
        super().__init__(
            name=name,
            max_speed=max_speed,
            wingspan=wingspan,
            max_altitude=max_altitude,
            num_passengers=num_passengers,
        )

        self.is_military = is_military
        self.afterburner_on = False
        self.autopilot_enabled = False
        self.mach_speed = 0.0  # current speed divided by speed of sound

        ObjectRegistry.add(self)

        logger.info(
            f"[JetPlane] '{self.name}' registered "
            f"(military={self.is_military}, wingspan={wingspan} ft, "
            f"max_alt={max_altitude} ft)"
        )

    # ---------------------------------------------------------
    # Speed & Afterburner
    # ---------------------------------------------------------
    def enable_afterburner(self):
        """Temporarily increase thrust and fuel/energy consumption."""
        if not self.in_air:
            logger.error("[JetPlane] Cannot enable afterburners while grounded.")
            return False

        self.afterburner_on = True
        logger.info(f"[JetPlane] {self.name} engaged afterburners! 🔥")
        return True

    def disable_afterburner(self):
        self.afterburner_on = False
        logger.info(f"[JetPlane] {self.name} disengaged afterburners.")
        return True

    def update_mach_speed(self, mph: float):
        """Convert MPH to Mach number for telemetry."""
        self.mach_speed = mph / self.SPEED_OF_SOUND_MPH
        logger.info(f"[JetPlane] {self.name} Mach={self.mach_speed:.2f}")

    # ---------------------------------------------------------
    # Combat / Aerobatic Maneuvers
    # ---------------------------------------------------------
    def barrel_roll(self):
        if not self.in_air:
            logger.error("[JetPlane] Cannot perform barrel roll on the ground.")
            return "Jet must be in the air."

        logger.warning(f"[JetPlane] {self.name} performs a BARREL ROLL! 🎯")
        return f"{self.name} performs a perfect barrel roll at {self.current_altitude} ft!"

    def immelmann(self):
        if not self.in_air:
            logger.error("[JetPlane] Cannot perform Immelmann while grounded.")
            return "Jet must be airborne."

        logger.info(f"[JetPlane] {self.name} performs an Immelmann turn.")
        return f"{self.name} performs an Immelmann and reverses direction!"

    # ---------------------------------------------------------
    # Auto-Pilot System
    # ---------------------------------------------------------
    def enable_autopilot(self):
        if not self.in_air:
            logger.error("[JetPlane] Cannot enable autopilot while grounded.")
            return False

        self.autopilot_enabled = True
        logger.info(f"[JetPlane] Auto-pilot engaged for {self.name}.")
        return True

    def disable_autopilot(self):
        self.autopilot_enabled = False
        logger.info(f"[JetPlane] Auto-pilot disengaged for {self.name}.")
        return True

    # ---------------------------------------------------------
    # Travel Override (for supersonic tracking)
    # ---------------------------------------------------------
    def travel(self, distance: float) -> bool:
        """Override to track Mach speed + afterburner."""
        logger.info(f"[JetPlane] {self.name} preparing supersonic travel: {distance} miles.")

        # If afterburner is enabled, max speed increases by 25%
        speed_used = self.max_speed * (1.25 if self.afterburner_on else 1.0)

        self.update_mach_speed(speed_used)

        return super().travel(distance)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "is_military": self.is_military,
                "afterburner_on": self.afterburner_on,
                "autopilot_enabled": self.autopilot_enabled,
                "mach_speed": self.mach_speed,
            }
        )
        return base

    def __str__(self):
        return (
            f"JetPlane(name={self.name}, Mach={self.mach_speed:.2f}, "
            f"afterburner={self.afterburner_on}, autopilot={self.autopilot_enabled}, "
            f"alt={self.current_altitude}, id={self.id})"
        )
