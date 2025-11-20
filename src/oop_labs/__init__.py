"""
OOP Labs Package
----------------

This package contains a collection of object-oriented models for vehicles,
aircraft, and transportation simulations used throughout the Software3-Lab
project.

Exports clean access to all major classes for IDE autocomplete,
tutorial usage, MCP integration, and unit-test discovery.
"""

from .transport_mode import TransportMode
from .motor_vehicle import MotorVehicle
from .motorcycle import Motorcycle
from .airplane import Airplane
from .jet_plane import JetPlane

__all__ = [
    "TransportMode",
    "MotorVehicle",
    "Motorcycle",
    "Airplane",
    "JetPlane",
]
