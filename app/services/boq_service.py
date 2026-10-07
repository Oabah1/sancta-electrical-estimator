from app import db
from app.models import BOQItem, ElectricalPoint


def calculate_amount(quantity, unit_price):
    return quantity * unit_price


def create_boq_item(
    project_id,
    description,
    specification,
    quantity,
    unit,
    unit_price,
    quantity_source=None,
):
    amount = calculate_amount(quantity, unit_price)

    boq_item = BOQItem(
        project_id=project_id,
        description=description,
        specification=specification,
        quantity=quantity,
        unit=unit,
        unit_price=unit_price,
        amount=amount,
        quantity_source=quantity_source,
    )

    db.session.add(boq_item)
    db.session.commit()

    return boq_item


def create_boq_from_electrical_point(
    project_id,
    point_type,
    quantity,
    unit,
    unit_price,
):
    return create_boq_item(
        project_id=project_id,
        description=point_type,
        specification=None,
        quantity=quantity,
        unit=unit,
        unit_price=unit_price,
        quantity_source="Electrical Point",
    )


def get_project_electrical_points(project_id):
    return ElectricalPoint.query.filter_by(project_id=project_id).all()


def generate_boq_from_electrical_points(project_id, unit_prices):
    electrical_points = get_project_electrical_points(project_id)

    boq_items = []

    for point in electrical_points:
        unit_price = unit_prices.get(point.point_type, 0)

        boq_item = create_boq_from_electrical_point(
            project_id=project_id,
            point_type=point.point_type,
            quantity=point.quantity,
            unit="pcs",
            unit_price=unit_price,
        )

        boq_items.append(boq_item)

    return boq_items


def calculate_boq_total(project_id):
    boq_items = BOQItem.query.filter_by(project_id=project_id).all()

    total = 0

    for item in boq_items:
        total += item.amount

    return total


def get_material_price(material_name):
    from app.models import MaterialPrice

    material_price = MaterialPrice.query.filter_by(
        material_name=material_name
    ).first()

    if material_price:
        return {
            "price": material_price.current_price,
            "unit": material_price.unit,
        }

    return {
        "price": 0,
        "unit": "pcs",
    }


def generate_boq_from_material_prices(project_id):
    clear_electrical_point_boq_items(project_id)

    electrical_points = get_project_electrical_points(project_id)

    boq_items = []

    for point in electrical_points:
        material_price = get_material_price(point.point_type)

        boq_item = create_boq_from_electrical_point(
            project_id=project_id,
            point_type=point.point_type,
            quantity=point.quantity,
            unit=material_price["unit"],
            unit_price=material_price["price"],
        )

        boq_items.append(boq_item)

    return boq_items


def clear_electrical_point_boq_items(project_id):
    boq_items = BOQItem.query.filter_by(
        project_id=project_id,
        quantity_source="Electrical Point",
    ).all()

    for item in boq_items:
        db.session.delete(item)

    db.session.commit()