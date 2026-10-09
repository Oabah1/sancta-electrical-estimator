import math

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