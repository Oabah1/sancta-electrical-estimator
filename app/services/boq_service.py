from app import db
from app.models import BOQItem


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