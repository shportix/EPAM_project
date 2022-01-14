"""
CRUD operations for position table file
"""
from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Position  # pylint: disable=import-error
from api import db, PositionSchema  # pylint: disable=import-error


positions_schema = PositionSchema(many=True)
position_schema = PositionSchema()


class PositionCRUD(Resource):
    """
    CRUD operations for position table
    """
    def get(self, position_id=None):  # pylint: disable=R0201
        """
        read method for position table
        """
        if position_id is not None:
            # get by id
            position = Position.query.get(position_id)
            if position:
                return make_response(position_schema.jsonify(position), 200)
            return make_response("position_not_found", 404)
        # get all
        all_positions = Position.query.all()
        result = positions_schema.dump(all_positions)
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for position table
        """
        position_name = request.form["position_name"]
        if Position.query.filter_by(position_name=position_name).first():
            return make_response("invalid_position_name", 400)
        new_position = Position(position_name=position_name)
        db.session.add(new_position)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        return make_response(position_schema.jsonify(new_position), 200)

    def put(self, position_id):  # pylint: disable=R0201
        """
        method tht updates position by id
        """
        position = Position.query.get(position_id)
        check_position = Position.query.filter_by(position_name=request.form["position_name"]).first()
        if check_position and check_position != position:
            return make_response("invalid_position_name", 400)
        if position:
            position.position_name = request.form["position_name"]
            db.commit()  # pylint: disable=E1101
            return make_response(position_schema.jsonify(position), 200)
        return make_response("position_not_found", 404)

    def delete(self, position_id):  # pylint: disable=R0201
        """
        delete method for position table
        """
        position = Position.query.get(position_id)
        if position:
            db.session.delete(position)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            return make_response(position_schema.jsonify(position), 200)
        return make_response("position_not_found", 404)
