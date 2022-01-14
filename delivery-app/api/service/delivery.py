"""
CRUD operations for delivery table file
"""
import datetime
from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Delivery, User, Employee, Department, Status, \
    Position  # pylint: disable=import-error
from api import db, DeliverySchema  # pylint: disable=import-error

deliveries_schema = DeliverySchema(many=True)
delivery_schema = DeliverySchema()


class DeliveryCRUD(Resource):
    """
    CRUD operations for delivery table
    """
    def get(self, delivery_id=None):  # pylint: disable=R0201
        """
        read method for delivery table
        """
        if delivery_id is not None:
            # get by id
            delivery = Delivery.query.get(delivery_id)
            if delivery:
                return make_response(delivery_schema.jsonify(delivery), 200)
            return make_response("delivery_not_found", 404)
        # get all
        all_deliveries = Delivery.query.all()
        result = deliveries_schema.dump(all_deliveries)
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for delivery table
        """
        department_id = int(request.form["department_id"])
        customer_id = int(request.form["customer_id"])
        courier_id = int(request.form["courier_id"])
        date = datetime.datetime.strptime(request.form["date"], '%Y/%m/%d')
        customer_address = request.form["customer_address"]
        status_id = int(request.form["status_id"])
        if not Department.query.get(department_id):
            return make_response("invalid_department_id", 400)
        customer = User.query.get(customer_id)
        courier = Employee.query.get(courier_id)
        if (not customer) or customer.isEmployee:
            return make_response("invalid_customer_id", 400)
        if (not courier) or (Position.query.get(courier.position_id).position_name != "courier"):
            return make_response("invalid_courier_id", 400)
        if not Status.query.get(status_id):
            return make_response("invalid_status_id", 400)
        new_delivery = Delivery(department_id=department_id,
                                customer_id=customer_id,
                                courier_id=courier_id,
                                date=date,
                                customer_address=customer_address,
                                status_id=status_id)
        db.session.add(new_delivery)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        return make_response(delivery_schema.jsonify(new_delivery), 200)

    def put(self, delivery_id):  # pylint: disable=R0201
        """
        method tht updates delivery by id
        """
        delivery = Delivery.query.get(delivery_id)
        if delivery:
            department_id = int(request.form["department_id"])
            customer_id = int(request.form["customer_id"])
            courier_id = int(request.form["courier_id"])
            date = datetime.datetime.strptime(request.form["date"], '%Y/%m/%d')
            customer_address = request.form["customer_address"]
            status_id = int(request.form["status_id"])
            if not Department.query.get(department_id):
                return make_response("invalid_department_id", 400)
            customer = User.query.get(customer_id)
            courier = Employee.query.get(courier_id)
            if (not customer) or customer.isEmployee:
                return make_response("invalid_customer_id", 400)
            if (not courier) or (
                    Position.query.get(courier.position_id).position_name != "courier"):
                return make_response("invalid_courier_id", 400)
            if not Status.query.get(status_id):
                return make_response("invalid_status_id", 400)
            delivery.department_id = department_id
            delivery.customer_id = customer_id
            delivery.courier_id = courier_id
            delivery.date = date
            delivery.customer_address = customer_address
            delivery.status_id = status_id
            db.session.commit()  # pylint: disable=E1101
            return make_response(delivery_schema.jsonify(delivery), 200)
        return make_response("delivery_not_found", 404)

    def delete(self, delivery_id):  # pylint: disable=R0201
        """
        delete method for delivery table
        """
        delivery = Delivery.query.get(delivery_id)
        if delivery:
            db.session.delete(delivery)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            return make_response(delivery_schema.jsonify(delivery), 200)
        return make_response("delivery_not_found", 404)
