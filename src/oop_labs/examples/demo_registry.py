"""
Demo: Object Registry + Inspection
----------------------------------

This script demonstrates how the ObjectRegistry registers and tracks all
instances of vehicles, airplanes, motorcycles, and jet planes.

Useful for:
- MCP server integration
- dashboards
- debugging
- simulation inspectors
- developer tools
"""

from pprint import pprint
from loguru import logger

from src.oop_labs.motorcycle import Motorcycle
from src.oop_labs.airplane import Airplane
from src.oop_labs.jet_plane import JetPlane
from src.core.object_registry import ObjectRegistry


def create_demo_objects():
    """Create a variety of transport mode objects and auto-register them."""
    logger.info("=== Creating demo objects for ObjectRegistry ===")

    m = Motorcycle(
        name="Harley Street 750",
        max_speed=110,
        horsepower=53,
        weight_lbs=514,
        seat_height=25.7,
        is_offroad_capable=False,
        has_abs=True,
    )
    m.configure_fuel_system(mpg=48, fuel_capacity=3.5)
    m.add_fuel(2.0)

    a = Airplane(
        name="Boeing 737",
        max_speed=588,
        wingspan=112,
        max_altitude=41000,
        num_passengers=189,
    )
    a.configure_fuel_system(mpg=0.2, fuel_capacity=6000)
    a.add_fuel(2000)
    a.takeoff()

    j = JetPlane(
        name="F-35 Lightning II",
        max_speed=1200,
        wingspan=35,
        max_altitude=50000,
        num_passengers=1,
        is_military=True,
    )
    j.configure_fuel_system(mpg=0.09, fuel_capacity=3000)
    j.add_fuel(800)
    j.takeoff()
    j.enable_afterburner()


def show_all_registered_objects():
    """Print out everything inside the registry in a clean JSON-table format."""
    logger.info("=== Listing all registered simulation objects ===")
    all_objects = ObjectRegistry.all()

    if not all_objects:
        print("No objects registered.")
        return

    print("\nRegistered Objects:")
    print("-------------------")
    for obj_id, obj in all_objects.items():
        print(f"ID: {obj_id} | Type: {obj.__class__.__name__}")
        pprint(obj.to_dict())
        print()


if __name__ == "__main__":
    logger.info("=== Running ObjectRegistry Demo ===\n")

    create_demo_objects()
    show_all_registered_objects()

    logger.info("\n=== Registry Demo Complete ===")
