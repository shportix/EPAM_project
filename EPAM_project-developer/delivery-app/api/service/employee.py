"""
CRUD operations for employee table file
"""
import datetime
import logging

from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Position, User, Employee, Department  # pylint: disable=import-error
from api import db, EmployeeSchema  # pylint: disable=import-error

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class EmployeeCRUD(Resource):
    """
    CRUD operations for employee table
    """

    def get(self, employee_id=None):  # pylint: disable=R0201
        """
        read method for employee table
        """
        if employee_id is not None:
            # get by id
            logging.info('Getting employee by id started')
            employee = Employee.query.get(employee_id)
            if employee:
                logging.info('Employee successfully found')
                return make_response(employee_schema.jsonify(employee), 200)
            logging.info('Getting employee by id failed: employee not found')
            return make_response("employee_not_found", 404)
        # get all
        logging.info('Getting all employees started')
        all_employees = Employee.query.all()
        result = employees_schema.dump(all_employees)
        logging.info('All employees successfully got')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for employee table
        """
        logging.info('Creation new employee started')
        position_id = int(request.form['position_id'])
        department_id = int(request.form['department_id'])
        birthday = datetime.datetime.strptime(request.form['birthday'], '%Y/%m/%d')
        salary = int(request.form['salary'])
        if not Position.query.get(position_id):
            logging.info('Creation new employee failed: invalid position id')
            return make_response("invalid_position_id", 400)
        if not Department.query.get(department_id):
            logging.info('Creation new employee failed: invalid department id')
            return make_response('invalid_department_id', 400)
        employee_id = request.form['id']
        user = User.query.get(employee_id)
        if not user:
            logging.info('Creation new employee failed: invalid user id')
            return make_response('invalid_user_id', 400)
        new_employee = Employee(id=employee_id,
                                position_id=position_id,
                                department_id=department_id,
                                birthday=birthday,
                                salary=salary)
        db.session.add(new_employee)  # pylint: disable=E1101
        user.isEmployee = True
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation new employee succeed')
        return make_response(employee_schema.jsonify(new_employee), 200)

    def put(self, employee_id):  # pylint: disable=R0201
        """
        method tht updates employee by id
        """
        logging.info('Update employee started')
        position_id = int(request.form['position_id'])
        department_id = int(request.form['department_id'])
        birthday = datetime.datetime.strptime(request.form['birthday'], '%Y/%m/%d')
        salary = int(request.form['salary'])
        if not Position.query.get(position_id):
            logging.info('Update employee failed: invalid position id')
            return make_response("invalid_position_id", 400)
        if not Department.query.get(department_id):
            logging.info('Update employee failed: invalid department id')
            return make_response('invalid_department_id', 400)
        employee = Employee.query.get(employee_id)
        if not employee:
            logging.info('Update employee failed: employee not found')
            return make_response('employee_not_found', 400)
        employee.salary = salary
        employee.birthday = birthday
        employee.department_id = department_id
        employee.position_id = position_id
        db.session.commit()  # pylint: disable=E1101
        logging.info('Update employee succeed')
        return make_response(employee_schema.jsonify(employee), 200)

    def delete(self, employee_id):  # pylint: disable=R0201
        """
        delete method for employee table
        """
        logging.info('Deletion employee started')
        employee = Employee.query.get(employee_id)
        user = User.query.get(employee_id)
        if employee:
            user.isEmployee = False
            db.session.delete(employee)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion employee succeed')
            return make_response(employee_schema.jsonify(employee), 200)
        logging.info('Deletion employee fail: employee not found')
        return make_response("employee_not_found", 404)
