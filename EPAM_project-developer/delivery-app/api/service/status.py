"""
CRUD operations for status table file
"""
import logging

from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Status  # pylint: disable=import-error
from api import db, StatusSchema  # pylint: disable=import-error

statuses_schema = StatusSchema(many=True)
status_schema = StatusSchema()


class StatusCRUD(Resource):
    """
    CRUD operations for status table
    """
    def get(self, status_id=None):  # pylint: disable=R0201
        """
        read method for status table
        """
        if status_id is not None:
            # get by id
            status = Status.query.get(status_id)
            logging.info('Getting status by id started')
            if status:
                logging.info('Status successfully found')
                return make_response(status_schema.jsonify(status), 200)
            logging.info('Getting status by id failed: status not found')
            return make_response("status_not_found", 404)
        # get all
        logging.info('Getting all statuses started')
        all_statuses = Status.query.all()
        result = statuses_schema.dump(all_statuses)
        logging.info('All statuses successfully got')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for status table
        """
        logging.info('Creation new status started')
        status_name = request.form["status_name"]
        new_status = Status(status_name=status_name)
        db.session.add(new_status)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation new status succeed')
        return make_response(status_schema.jsonify(new_status), 200)

    def put(self, status_id):  # pylint: disable=R0201
        """
        method tht updates status by id
        """
        logging.info('Update status started')
        status = Status.query.get(status_id)
        if status:
            status.status_name = request.form["status_name"]
            db.session.commit()  # pylint: disable=E1101
            logging.info('Update status succeed')
            return make_response(status_schema.jsonify(status), 200)
        logging.info('Update status failed: status not found')
        return make_response("status_not_found", 404)

    def delete(self, status_id):  # pylint: disable=R0201
        """
        delete method for status table
        """
        logging.info('Deletion status started')
        status = Status.query.get(status_id)
        if status:
            db.session.delete(status)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion status succeed')
            return make_response(status_schema.jsonify(status), 200)
        logging.info('Deletion status fail: status not found')
        return make_response("status_not_found", 404)
