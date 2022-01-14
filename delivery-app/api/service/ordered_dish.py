"""
CRUD operations for order table file
"""
from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import OrderedDish, Delivery, Dish, Status  # pylint: disable=import-error
from api import db, OrderSchema  # pylint: disable=import-error

orders_schema = OrderSchema(many=True)
order_schema = OrderSchema()


class OrderedDishCRUD(Resource):
    """
    CRUD operations for order table
    """

    def get(self, order_id=None):  # pylint: disable=R0201
        """
        read method for order table
        """
        if order_id is not None:
            # get by id
            order = OrderedDish.query.get(order_id)
            if order:
                return make_response(order_schema.jsonify(order), 200)
            return make_response("order_not_found", 404)
        # get all
        all_orders = OrderedDish.query.all()
        result = orders_schema.dump(all_orders)
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for order table
        """
        delivery_id = int(request.form["delivery_id"])
        dish_id = int(request.form["dish_id"])
        status_id = int(request.form["status_id"])
        if not Delivery.query.get(delivery_id):
            return make_response("invalid_delivery_id", 400)
        if not Dish.query.get(dish_id):
            return make_response("invalid_dish_id", 400)
        if not Status.query.get(status_id):
            return make_response("invalid_status_id", 400)
        new_order = OrderedDish(delivery_id=delivery_id,
                                dish_id=dish_id,
                                status_id=status_id)
        db.session.add(new_order)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        return make_response(order_schema.jsonify(new_order), 200)

    def put(self, order_id):  # pylint: disable=R0201
        """
        method that updates order by id
        """
        order = OrderedDish.query.get(order_id)
        delivery_id = int(request.form["delivery_id"])
        dish_id = int(request.form["dish_id"])
        status_id = int(request.form["status_id"])
        if not Delivery.query.get(delivery_id):
            return make_response("invalid_delivery_id", 400)
        if not Dish.query.get(dish_id):
            return make_response("invalid_dish_id", 400)
        if not Status.query.get(status_id):
            return make_response("invalid_status_id", 400)
        if order:
            order.delivery_id = delivery_id
            order.dish_id = dish_id
            order.status_id = status_id
            db.session.commit()  # pylint: disable=E1101
            return make_response(order_schema.jsonify(order), 200)
        return make_response("order_not_found", 404)

    def delete(self, order_id):  # pylint: disable=R0201
        """
        delete method for order table
        """
        order = OrderedDish.query.get(order_id)
        if order:
            db.session.delete(order)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            return make_response(order_schema.jsonify(order), 200)
        return make_response("order_not_found", 404)
