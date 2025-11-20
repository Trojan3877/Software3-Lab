from __future__ import annotations
from typing import Optional, Dict, Any
from loguru import logger

from src.oop_labs.transport_mode import TransportMode
from src.core.object_registry import ObjectRegistry


class MotorVehicle(TransportMode):
    """
    Represents a generic motor vehicle (car, truck, motorcycle, ATV, etc.)

    Features:
    ---------
    - Supports fuel-based OR electric-battery-based power systems
    - Adds horsepower + weight for future ML integration
    - Tracks engine state and allows start/stop
    - Provides range estimation, energy usage simulation
    - Logs all events for ML/AI/MCP and debugging
    """

    def __init__(
        self,
        name: str,
        max_speed: float,
        horsepower: Optional[int] = None,
        weight_lbs: Optional[float] = None,
    ):
        super().__init__(name=name, max_speed=max_speed)

        # Vehicle-specific attributes
        self.horsepower = horsepower
        self.weight_lbs = weight_lbs

        # State
        self.engine_running: bool = False

        # Optional EV system
        self.battery_kwh: Optional[float] = None
        self.current_charge_kwh: Optional[float] = None
        self.efficiency_mi_per_kwh: Optional[float] = None

        ObjectRegistry.add(self)

        logger.info(
            f"[MotorVehicle] Registered vehicle '{self.name}' "
            f"(hp={self.horsepower}, weight={self.weight_lbs} lbs)"
        )

    # ---------------------------------------------------------
    # Engine System
    # ---------------------------------------------------------
    def start_engine(self):
        if self.engine_running:
            logger.warning(f"[MotorVehicle] {self.name} engine already running.")
            return False

        self.engine_running = True
        logger.info(f"[MotorVehicle] {self.name} engine started.")
        return True

    def stop_engine(self):
        if not self.engine_running:
            logger.warning(f"[MotorVehicle] {self.name} engine already off.")
            return False

        self.engine_running = False
        logger.info(f"[MotorVehicle] {self.name} engine stopped.")
        return True

    # ---------------------------------------------------------
    # Electric Vehicle System
    # ---------------------------------------------------------
    def configure_ev_system(self, battery_kwh: float, efficiency_mi_per_kwh: float):
        """Enable EV energy system."""
        self.battery_kwh = battery_kwh
        self.current_charge_kwh = 0.0
        self.efficiency_mi_per_kwh = efficiency_mi_per_kwh

        logger.info(
            f"[MotorVehicle] {self.name} configured as an EV "
            f"(battery={battery_kwh} kWh, efficiency={efficiency_mi_per_kwh} mi/kWh)"
        )

    def charge(self, kwh: float):
        if self.current_charge_kwh is None:
            raise RuntimeError("EV system not configured for this vehicle.")
        if kwh <= 0:
            logger.warning("[MotorVehicle] Cannot charge with negative or zero kWh.")
            return

        new_charge = min(self.battery_kwh, self.current_charge_kwh + kwh)
        logger.info(
            f"[MotorVehicle] Charging {self.name}: "
            f"{self.current_charge_kwh} -> {new_charge} kWh"
        )
        self.current_charge_kwh = new_charge

    def remaining_range_ev(self) -> Optional[float]:
        if self.current_charge_kwh is None or self.efficiency_mi_per_kwh is None:
            return None
        return self.current_charge_kwh * self.efficiency_mi_per_kwh

    # ---------------------------------------------------------
    # Travel override — supports gas OR EV
    # ---------------------------------------------------------
    def travel(self, distance: float) -> bool:
        """Simulate travel using the appropriate power system."""
        if distance <= 0:
            logger.warning("[MotorVehicle] Distance must be positive.")
            return False

        # EV takes priority if configured
        if self.efficiency_mi_per_kwh is not None:
            required_kwh = distance / self.efficiency_mi_per_kwh
            if self.current_charge_kwh < required_kwh:
                logger.error(
                    f"[MotorVehicle] {self.name} cannot travel {distance} miles (EV). "
                    f"Required={required_kwh:.2f} kWh, Available={self.current_charge_kwh:.2f} kWh"
                )
                return False

            self.current_charge_kwh -= required_kwh
            logger.info(
                f"[MotorVehicle] {self.name} traveled {distance} miles using EV power. "
                f"Remaining charge={self.current_charge_kwh:.2f} kWh"
            )
            return True

        # Otherwise use fuel-based system from TransportMode
        return super().travel(distance)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "horsepower": self.horsepower,
                "weight_lbs": self.weight_lbs,
                "engine_running": self.engine_running,
                "battery_kwh": self.battery_kwh,
                "current_charge_kwh": self.current_charge_kwh,
                "efficiency_mi_per_kwh": self.efficiency_mi_per_kwh,
                "ev_range_estimate": self.remaining_range_ev(),
            }
        )
        return base

    def __str__(self):
        return (
            f"MotorVehicle(name={self.name}, hp={self.horsepower}, weight={self.weight_lbs}, "
            f"engine_running={self.engine_running}, fuel={self.current_fuel}, "
            f"charge={self.current_charge_kwh} kWh, id={self.id})"
        )
