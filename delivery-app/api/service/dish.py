"""
CRUD operations for dish table file
"""
from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Dish, DishCategory, Image  # pylint: disable=import-error
from api import db, DishSchema  # pylint: disable=import-error

dishes_schema = DishSchema(many=True)
dish_schema = DishSchema()


class DishCRUD(Resource):
    """
    CRUD operations for dish table
    """

    def get(self, dish_id=None):  # pylint: disable=R0201
        """
        method that gets dish id nd returns dish
        """
        if dish_id is not None:
            dish = Dish.query.get(dish_id)
            if dish:
                return make_response(dish_schema.jsonify(dish), 200)
            return make_response("dish_not_found", 404)
        all_dishes = Dish.query.all()
        result = dishes_schema.dump(all_dishes)
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for dish table
        """
        category_id = int(request.form["category_id"])
        dish_name = request.form["dish_name"]
        cost_price = int(request.form["cost_price"])
        value_added = int(request.form["value_added"])
        image_id = int(request.form["image_id"])
        description = request.form["description"]
        if not DishCategory.query.get(category_id):
            return make_response("invalid_category_id", 400)
        if not Image.query.get(image_id):
            return make_response("invalid_image_id")
        new_dish = Dish(category_id=category_id,
                        dish_name=dish_name,
                        cost_price=cost_price,
                        value_added=value_added,
                        image_id=image_id,
                        description=description)
        db.session.add(new_dish)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        return make_response(dish_schema.jsonify(new_dish), 200)

    def put(self, dish_id):  # pylint: disable=R0201
        """
        method tht updates dish by id
        """
        dish = Dish.query.get(dish_id)
        if dish:
            category_id = int(request.form["category_id"])
            dish_name = request.form["dish_name"]
            cost_price = int(request.form["cost_price"])
            value_added = int(request.form["value_added"])
            image_id = int(request.form["image_id"])
            description = request.form["description"]
            if not DishCategory.query.get(category_id):
                return make_response("invalid_category_id", 400)
            if not Image.query.get(image_id):
                return make_response("invalid_image_id")
            dish.category_id = category_id
            dish.dish_name = dish_name
            dish.cost_price = cost_price
            dish.value_added = value_added
            dish.image_id = image_id
            dish.description = description
            db.commit()  # pylint: disable=E1101
            return make_response(dish_schema.jsonify(dish), 200)
        return make_response("dish_not_found", 404)

    def delete(self, dish_id):  # pylint: disable=R0201
        """
        delete method for dish table
        """
        dish = Dish.query.get(dish_id)
        if dish:
            db.session.delete(dish)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            return make_response(dish_schema.jsonify(dish), 200)
        return make_response("dish_not_found", 404)
