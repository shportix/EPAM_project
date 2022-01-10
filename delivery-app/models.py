"""
database models
"""
from sqlalchemy.sql import func
from app import db


class Position(db.Model):  # pylint: disable=too-few-public-methods
    """
    position table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    position_name = db.Column(db.String(100), unique=True)  # pylint: disable=E1101


class User(db.Model):  # pylint: disable=too-few-public-methods
    """
    user table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    email = db.Column(db.String(100), nullable=False, unique=True)  # pylint: disable=E1101
    password = db.Column(db.String(100), nullable=False)  # pylint: disable=E1101
    name = db.Column(db.String(100), nullable=True)  # pylint: disable=E1101
    surname = db.Column(db.String(100), nullable=True)  # pylint: disable=E1101
    phoneNumber = db.Column(db.String(50), nullable=True)  # pylint: disable=E1101
    isEmployee = db.Column(db.Boolean, default=False)  # pylint: disable=E1101


class Department(db.Model):  # pylint: disable=too-few-public-methods
    """
    Department table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    name = db.Column(db.String(100), nullable=True)  # pylint: disable=E1101
    city = db.Column(db.String(100), nullable=False)  # pylint: disable=E1101
    address = db.Column(db.String(200), nullable=False)  # pylint: disable=E1101


class Employee(db.Model):  # pylint: disable=too-few-public-methods
    """
    Employee table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)  # pylint: disable=E1101
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"), nullable=False)  # pylint: disable=E1101
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)  # pylint: disable=E1101
    birthday = db.Column(db.Date, nullable=False)  # pylint: disable=E1101
    salary = db.Column(db.Integer, nullable=False)  # pylint: disable=E1101


class Image(db.Model):  # pylint: disable=too-few-public-methods
    """
    image table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    img = db.Column(db.Text)  # pylint: disable=E1101
    name = db.Column(db.String(200), nullable=False)  # pylint: disable=E1101
    mimetype = db.Column(db.String(200), nullable=False)  # pylint: disable=E1101


class DishCategory(db.Model):  # pylint: disable=too-few-public-methods
    """
    dish category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    category_name = db.Column(db.String(100), unique=True)  # pylint: disable=E1101


class Dish(db.Model):  # pylint: disable=too-few-public-methods
    """
    dish table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('dish_category.id'))  # pylint: disable=E1101
    dish_name = db.Column(db.String(100), unique=True, nullable=False)  # pylint: disable=E1101
    cost_price = db.Column(db.Integer, nullable=False)  # pylint: disable=E1101
    value_added = db.Column(db.Integer, nullable=False)  # pylint: disable=E1101
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # pylint: disable=E1101
    description = db.Column(db.Text, nullable=False)  # pylint: disable=E1101


class Status(db.Model):  # pylint: disable=too-few-public-methods
    """
    status category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    status_name = db.Column(db.String(100), unique=True)  # pylint: disable=E1101


class Delivery(db.Model):  # pylint: disable=too-few-public-methods
    """
    delivery category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)  # pylint: disable=E1101
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # pylint: disable=E1101
    courier_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)  # pylint: disable=E1101
    date = db.Column(db.Date, default=func.now())  # pylint: disable=E1101
    customer_address = db.Column(db.Text, nullable=False)  # pylint: disable=E1101
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))  # pylint: disable=E1101


class Order(db.Model):  # pylint: disable=too-few-public-methods
    """
    order category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=E1101
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=True)  # pylint: disable=E1101
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)  # pylint: disable=E1101
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))  # pylint: disable=E1101
