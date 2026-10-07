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
    brand = db.Column(db.String(100), nullable=True)
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