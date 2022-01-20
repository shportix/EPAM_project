"""
CRUD operations for department table file
"""
import logging
from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Department  # pylint: disable=import-error
from api import db, DepartmentSchema  # pylint: disable=import-error


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


class DepartmentCRUD(Resource):
    """
    CRUD operations for department table
    """

    def get(self, department_id=None):  # pylint: disable=R0201
        """
        read method for department table
        """
        if department_id is not None:
            # get by id
            logging.info('Getting department by id started')
            department = Department.query.get(department_id)
            if department:
                logging.info('Department successfully found!')
                return make_response(department_schema.jsonify(department), 200)
            logging.info('Getting department by id failed: department not found!')
            return make_response("department_not_found", 404)
        # get all
        logging.info('Getting all departments started')
        all_departments = Department.query.all()
        result = departments_schema.dump(all_departments)
        logging.info('All departments successfully got!')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for department table
        """
        logging.info('Creation new department started')
        name = request.form["name"]
        city = request.form['city']
        address = request.form['address']
        new_department = Department(name=name,
                                    city=city,
                                    address=address,)
        db.session.add(new_department)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation new department succeed')
        return make_response(department_schema.jsonify(new_department), 200)

    def put(self, department_id):  # pylint: disable=R0201
        """
        method tht updates department by id
        """
        logging.info('Update department started')
        department = Department.query.get(department_id)
        if department:
            department.name = request.form["name"]
            department.city = request.form["city"]
            department.address = request.form["address"]
            db.session.commit()  # pylint: disable=E1101
            logging.info('Update department succeed')
            return make_response(department_schema.jsonify(department), 200)
        logging.info('Update department failed: department not found')
        return make_response("department_not_found", 404)

    def delete(self, department_id):  # pylint: disable=R0201
        """
        delete method for department table
        """
        logging.info('Deletion department started')
        department = Department.query.get(department_id)
        if department:
            db.session.delete(department)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion department succeed')
            return make_response(department_schema.jsonify(department), 200)
        logging.info('Deletion department fail: department not found')
        return make_response("department_not_found", 404)
