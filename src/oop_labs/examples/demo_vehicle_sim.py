"""
Demo Vehicle Simulation
-----------------------

This script demonstrates how to use the OOP classes in the oop_labs package:
- TransportMode
- MotorVehicle
- Motorcycle
- Airplane
- JetPlane

Run this demo to see inheritance, polymorphism, logging, and simulation functions.
"""

from loguru import logger

from src.oop_labs.motorcycle import Motorcycle
from src.oop_labs.airplane import Airplane
from src.oop_labs.jet_plane import JetPlane


def demo_motorcycle():
    logger.info("=== Motorcycle Demo ===")

    bike = Motorcycle(
        name="Kawasaki Ninja ZX-6R",
        max_speed=165,
        horsepower=130,
        weight_lbs=430,
        seat_height=32.7,
        is_offroad_capable=False,
        has_abs=True
    )

    bike.start_engine()
    bike.configure_fuel_system(mpg=42, fuel_capacity=5.0)
    bike.add_fuel(3.0)

    bike.travel(40)
    bike.wheelie()
    bike.lean(35)
    bike.lean(60)  # unsafe lean


def demo_airplane():
    logger.info("=== Airplane Demo ===")

    plane = Airplane(
        name="Cessna 172",
        max_speed=140,
        wingspan=36,
        max_altitude=13000,
        num_passengers=4
    )

    plane.configure_fuel_system(mpg=15, fuel_capacity=50)
    plane.add_fuel(20)

    plane.takeoff()
    plane.climb(3000)
    plane.climb(6000)
    plane.descend(7000)
    plane.land()

    plane.travel(100)


def demo_jetplane():
    logger.info("=== JetPlane Demo ===")

    jet = JetPlane(
        name="F-22 Raptor",
        max_speed=1500,
        wingspan=44.5,
        max_altitude=65000,
        num_passengers=1,
        is_military=True,
    )

    jet.configure_fuel_system(mpg=2, fuel_capacity=300)  # jet fuel burn rate
    jet.add_fuel(200)

    jet.takeoff()
    jet.climb(10000)
    jet.enable_afterburner()
    jet.travel(50)

    jet.barrel_roll()
    jet.immelmann()

    jet.disable_afterburner()
    jet.descend(15000)
    jet.land()


if __name__ == "__main__":
    logger.info("=== Running OOP Vehicle Simulation Demo ===\n")

    demo_motorcycle()
    print("\n----------------------------------------\n")

    demo_airplane()
    print("\n----------------------------------------\n")

    demo_jetplane()

    logger.info("=== Demo Complete ===")
