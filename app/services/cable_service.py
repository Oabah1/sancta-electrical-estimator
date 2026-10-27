import math

from app import db
from app.models import Cable


def calculate_coils(required_metres, coil_length):
    """
    Calculate the number of complete cable coils required.
    """

    if required_metres < 0:
        raise ValueError("Required cable length cannot be negative.")

    if coil_length <= 0:
        raise ValueError("Coil length must be greater than zero.")

    number_of_coils = math.ceil(required_metres / coil_length)
    supplied_metres = number_of_coils * coil_length
    spare_metres = supplied_metres - required_metres

    return {
        "required_metres": required_metres,
        "coil_length": coil_length,
        "number_of_coils": number_of_coils,
        "supplied_metres": supplied_metres,
        "spare_metres": spare_metres,
    }


def calculate_cable_cost(cable, required_metres):
    """
    Calculate the coils and cost for one cable record.
    """

    result = calculate_coils(
        required_metres,
        cable.coil_length,
    )

    price_per_coil = cable.unit_price or 0

    result.update({
        "cable_id": cable.id,
        "cable_type": cable.cable_type,
        "size": cable.size,
        "colour": cable.colour,
        "function": cable.function,
        "price_per_coil": price_per_coil,
        "total_cost": result["number_of_coils"] * price_per_coil,
    })

    return result


def calculate_project_cable_cost(cable_requirements):
    """
    Calculate cable coils and costs for multiple cable records.

    cable_requirements is a dictionary mapping cable IDs
    to their separately estimated required lengths in metres.

    Example:
        {1: 635, 2: 600, 3: 500}
    """

    results = []

    for cable_id, required_metres in cable_requirements.items():
        cable = Cable.query.get(cable_id)

        if cable is None:
            raise ValueError(f"Cable record {cable_id} was not found.")

        result = calculate_cable_cost(cable, required_metres)
        results.append(result)

    return {
        "cables": results,
        "total_cost": sum(item["total_cost"] for item in results),
    }

def estimate_circuit_conductor_length(route_length, conductor_count, allowance_percent=10):
    """
    Estimate total conductor length for a circuit route.

    This is a preliminary quantity estimate, not an electrical
    cable-sizing calculation.
    """

    if route_length < 0:
        raise ValueError("Route length cannot be negative.")

    if conductor_count < 1:
        raise ValueError("Conductor count must be at least 1.")

    if allowance_percent < 0:
        raise ValueError("Allowance percentage cannot be negative.")

    base_length = route_length * conductor_count
    allowance_length = base_length * allowance_percent / 100
    estimated_length = base_length + allowance_length

    return {
        "route_length": route_length,
        "conductor_count": conductor_count,
        "allowance_percent": allowance_percent,
        "base_length": base_length,
        "allowance_length": allowance_length,
        "estimated_length": estimated_length,
    }


def estimate_circuit_from_database(circuit_id, conductor_count, allowance_percent=10):
    """
    Estimate conductor length using a circuit saved in the database.
    """

    from app.models import Circuit

    circuit = db.session.get(Circuit, circuit_id)

    if circuit is None:
        raise ValueError(f"Circuit record {circuit_id} was not found.")

    if circuit.route_length is None:
        raise ValueError(
            f"Circuit '{circuit.circuit_name}' has no route length."
        )

    result = estimate_circuit_conductor_length(
        route_length=circuit.route_length,
        conductor_count=conductor_count,
        allowance_percent=allowance_percent,
    )

    result.update({
        "circuit_id": circuit.id,
        "circuit_name": circuit.circuit_name,
        "circuit_type": circuit.circuit_type,
    })

    return result


def estimate_circuit_cable_cost(
    circuit_id,
    cable_id,
    conductor_count,
    allowance_percent=10,
):
    """
    Estimate cable quantity and cost for a saved circuit.

    This estimates conductor length and coil cost only.
    It does not determine whether the cable size is electrically suitable.
    """
    from app.models import Circuit

    circuit = db.session.get(Circuit, circuit_id)

    if circuit is None:
        raise ValueError(f"Circuit record {circuit_id} was not found.")

    if circuit.route_length is None:
        raise ValueError(
            f"Circuit '{circuit.circuit_name}' has no route length."
        )

    cable = db.session.get(Cable, cable_id)

    if cable is None:
        raise ValueError(f"Cable record {cable_id} was not found.")

    length_estimate = estimate_circuit_conductor_length(
        route_length=circuit.route_length,
        conductor_count=conductor_count,
        allowance_percent=allowance_percent,
    )

    cable_cost = calculate_cable_cost(
        cable,
        length_estimate["estimated_length"],
    )

    return {
        "project_id": circuit.project_id,
        "circuit_id": circuit.id,
        "circuit_name": circuit.circuit_name,
        "circuit_type": circuit.circuit_type,
        "length_estimate": length_estimate,
        "cable_cost": cable_cost,
    }
