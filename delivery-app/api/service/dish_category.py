"""
CRUD operations for dish category table file
"""
import logging

from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import DishCategory  # pylint: disable=import-error
from api import db, DishCategorySchema  # pylint: disable=import-error

dish_categories_schema = DishCategorySchema(many=True)
dish_category_schema = DishCategorySchema()


class DishCategoryCRUD(Resource):
    """
    CRUD operations for dish category table
    """

    def get(self, dish_category_id=None):  # pylint: disable=R0201
        """
        read method for dish category table
        """
        if dish_category_id is not None:
            # get by id
            logging.info('Getting dish category by id started')
            dish_category = DishCategory.query.get(dish_category_id)
            if dish_category:
                logging.info('Dish category successfully found')
                return make_response(dish_category_schema.jsonify(dish_category), 200)
            logging.info('Getting dish category by id failed: dish category not found')
            return make_response("dish_category_not_found", 404)
        # get all
        logging.info('Getting all dish categories started')
        all_dish_categories = DishCategory.query.all()
        result = dish_categories_schema.dump(all_dish_categories)
        logging.info('All dish categories successfully got')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for dish category table
        """
        logging.info('Creation new dish category started')
        new_dish_category = DishCategory(category_name=request.form["category_name"])
        db.session.add(new_dish_category)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation new dish category succeed')
        return make_response(dish_category_schema.jsonify(new_dish_category), 200)

    def put(self, dish_category_id):  # pylint: disable=R0201
        """
        method tht updates dish category by id
        """
        logging.info('Update dish category started')
        dish_category = DishCategory.query.get(dish_category_id)
        if dish_category:
            dish_category.category_name = request.form["category_name"]
            db.session.commit()  # pylint: disable=E1101
            logging.info('Update dish category succeed')
            return make_response(dish_category_schema.jsonify(dish_category), 200)
        logging.info('Update dish category failed: dish category not found')
        return make_response("dish_category_not_found", 404)

    def delete(self, dish_category_id):  # pylint: disable=R0201
        """
        delete method for dish category table
        """
        logging.info('Deletion dish category started')
        dish_category = DishCategory.query.get(dish_category_id)
        if dish_category:
            db.session.delete(dish_category)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion dish category succeed')
            return make_response(dish_category_schema.jsonify(dish_category), 200)
        logging.info('Deletion dish category fail: dish category not found')
        return make_response("dish_category_not_found", 404)
