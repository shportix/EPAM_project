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
    position_name = db.Column(db.String(100), unique=True)


class User(db.Model):  # pylint: disable=too-few-public-methods
    """
    user table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    surname = db.Column(db.String(100), nullable=True)
    phoneNumber = db.Column(db.String(50), nullable=True)
    isEmployee = db.Column(db.Boolean, default=False)


class Department(db.Model):  # pylint: disable=too-few-public-methods
    """
    Department table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)


class Employee(db.Model):  # pylint: disable=too-few-public-methods
    """
    Employee table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    birthday = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)


class Image(db.Model):  # pylint: disable=too-few-public-methods
    """
    image table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text)
    name = db.Column(db.String(200), nullable=False)
    mimetype = db.Column(db.String(200), nullable=False)


class DishCategory(db.Model):  # pylint: disable=too-few-public-methods
    """
    dish category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)


class Dish(db.Model):  # pylint: disable=too-few-public-methods
    """
    dish table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('dish_category.id'))
    dish_name = db.Column(db.String(100), unique=True, nullable=False)
    cost_price = db.Column(db.Integer, nullable=False)
    value_added = db.Column(db.Integer, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    description = db.Column(db.Text, nullable=False)


class Status(db.Model):  # pylint: disable=too-few-public-methods
    """
    status category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100), unique=True)


class Delivery(db.Model):  # pylint: disable=too-few-public-methods
    """
    delivery category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, default=func.now())
    customer_address = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))


class Order(db.Model):  # pylint: disable=too-few-public-methods
    """
    order category table model
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
