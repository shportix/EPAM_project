"""
CRUD operations for order table file
"""
import logging

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
        read method for ordered dish table
        """
        if order_id is not None:
            # get by id
            logging.info('Getting ordered dish by id started')
            order = OrderedDish.query.get(order_id)
            if order:
                logging.info('Ordered dish successfully found')
                return make_response(order_schema.jsonify(order), 200)
            return make_response("order_not_found", 404)
        # get all
        logging.info('Getting all ordered dishes started')
        all_orders = OrderedDish.query.all()
        result = orders_schema.dump(all_orders)
        logging.info('All ordered dishes successfully got')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for ordered dish table
        """
        logging.info('Creation new ordered dish started')
        delivery_id = int(request.form["delivery_id"])
        dish_id = int(request.form["dish_id"])
        status_id = int(request.form["status_id"])
        if not Delivery.query.get(delivery_id):
            logging.info('Creation new ordered dish failed: invalid delivery id')
            return make_response("invalid_delivery_id", 400)
        if not Dish.query.get(dish_id):
            logging.info('Creation new ordered dish failed: invalid dish id')
            return make_response("invalid_dish_id", 400)
        if not Status.query.get(status_id):
            logging.info('Creation new ordered dish failed: invalid status id')
            return make_response("invalid_status_id", 400)
        new_order = OrderedDish(delivery_id=delivery_id,
                                dish_id=dish_id,
                                status_id=status_id)
        db.session.add(new_order)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation new ordered dish succeed')
        return make_response(order_schema.jsonify(new_order), 200)

    def put(self, order_id):  # pylint: disable=R0201
        """
        method that updates ordered dish by id
        """
        logging.info('Update ordered dish started')
        order = OrderedDish.query.get(order_id)
        delivery_id = int(request.form["delivery_id"])
        dish_id = int(request.form["dish_id"])
        status_id = int(request.form["status_id"])
        if not Delivery.query.get(delivery_id):
            logging.info('Update ordered dish failed: invalid delivery id')
            return make_response("invalid_delivery_id", 400)
        if not Dish.query.get(dish_id):
            logging.info('Update ordered dish failed: invalid dish id')
            return make_response("invalid_dish_id", 400)
        if not Status.query.get(status_id):
            logging.info('Update ordered dish failed: invalid status id')
            return make_response("invalid_status_id", 400)
        if order:
            order.delivery_id = delivery_id
            order.dish_id = dish_id
            order.status_id = status_id
            db.session.commit()  # pylint: disable=E1101
            logging.info('Update ordered dish succeed')
            return make_response(order_schema.jsonify(order), 200)
        logging.info('Update ordered dish failed: ordered dish not found')
        return make_response("order_not_found", 404)

    def delete(self, order_id):  # pylint: disable=R0201
        """
        delete method for ordered dish table
        """
        logging.info('Deletion ordered dish started')
        order = OrderedDish.query.get(order_id)
        if order:
            db.session.delete(order)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion ordered dish succeed')
            return make_response(order_schema.jsonify(order), 200)
        logging.info('Deletion ordered dish fail: ordered dish not found')
        return make_response("ordered_dish_not_found", 404)
