from datetime import datetime

from app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    building_type = db.Column(db.String(100), nullable=False)
    number_of_floors = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Estimation")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)


class ElectricalPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    point_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.String(200), nullable=True)
    load_watts = db.Column(db.Float, nullable=True)


class Fitting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    default_rating = db.Column(db.String(50), nullable=True)
    default_load = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(50), nullable=False, default="pcs")
    description = db.Column(db.String(200), nullable=True)


class Cable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cable_type = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    conductor_material = db.Column(db.String(100), nullable=True)
    insulation = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(50), nullable=False)
    colour = db.Column(db.String(50), nullable=False)
    function = db.Column(db.String(50), nullable=False)
    coil_length = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=True)
    stock_quantity = db.Column(db.Float, nullable=True, default=0)


class Circuit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    circuit_name = db.Column(db.String(100), nullable=False)
    circuit_type = db.Column(db.String(100), nullable=False)
    connected_load = db.Column(db.Float, nullable=True, default=0)
    design_load = db.Column(db.Float, nullable=True, default=0)
    design_current = db.Column(db.Float, nullable=True, default=0)
    cable_size = db.Column(db.String(50), nullable=True)
    protection_rating = db.Column(db.String(50), nullable=True)
    route_length = db.Column(db.Float, nullable=True)


class ProtectionDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(50), nullable=False)
    poles = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=True, default=0)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="Technician")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MaterialPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String(150), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(150), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Labour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    calculation_method = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BOQItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    specification = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    amount = db.Column(db.Float, nullable=False, default=0)
    quantity_source = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProjectMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False,
        index=True,
    )
    material_name = db.Column(db.String(150), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    amount = db.Column(db.Float, nullable=False, default=0)
    category = db.Column(db.String(80), nullable=False, default="Piping")
    notes = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class ProjectCableEstimate(db.Model):
    """Cable estimate with saved specifications for catalogue or manual entries."""

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False,
        index=True,
    )
    cable_id = db.Column(
        db.Integer,
        db.ForeignKey("cable.id"),
        nullable=True,
    )

    # Saved cable details: these remain available even if the catalogue changes.
    cable_type = db.Column(db.String(150), nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(50), nullable=True)
    colour = db.Column(db.String(50), nullable=True)
    function = db.Column(db.String(100), nullable=True)
    conductor_material = db.Column(db.String(100), nullable=True)
    insulation = db.Column(db.String(100), nullable=True)

    required_metres = db.Column(db.Float, nullable=False)
    coil_length = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    project = db.relationship("Project")
    cable = db.relationship("Cable")


class RoomFitting(db.Model):
    """A fitting assigned to a room, with its project-specific price."""

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("room.id"),
        nullable=False,
        index=True,
    )

    fitting_id = db.Column(
        db.Integer,
        db.ForeignKey("fitting.id"),
        nullable=False,
        index=True,
    )

    quantity = db.Column(db.Float, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0)

    room = db.relationship("Room")
    fitting = db.relationship("Fitting")

    @property
    def amount(self):
        return self.quantity * self.unit_price
