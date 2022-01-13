"""
CRUD operations for employee table file
"""
import datetime
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
        method that gets employee id nd returns employee
        """
        if employee_id is not None:
            employee = Employee.query.get(employee_id)
            if employee:
                return make_response(employee_schema.jsonify(employee), 200)
            return make_response("employee_not_found", 404)
        all_employees = Employee.query.all()
        result = employees_schema.dump(all_employees)
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for employee table
        """
        position_id = int(request.form['position_id'])
        department_id = int(request.form['department_id'])
        birthday = datetime.datetime.strptime(request.form['birthday'], '%Y/%m/%d')
        salary = int(request.form['salary'])
        if not Position.query.get(position_id):
            return make_response("invalid_position_id", 400)
        if not Department.query.get(department_id):
            return make_response('invalid_department_id', 400)
        employee_id = request.form['id']
        user = User.query.get(employee_id)
        if not user:
            return make_response('invalid_user_id', 400)
        new_employee = Employee(id=employee_id,
                                position_id=position_id,
                                department_id=department_id,
                                birthday=birthday,
                                salary=salary)
        db.session.add(new_employee)  # pylint: disable=E1101
        user.isEmployee = True
        db.session.commit()  # pylint: disable=E1101
        return make_response(employee_schema.jsonify(new_employee), 200)

    def put(self, employee_id):  # pylint: disable=R0201
        """
        method tht updates employee by id
        """
        position_id = int(request.form['position_id'])
        department_id = int(request.form['department_id'])
        birthday = datetime.datetime.strptime(request.form['birthday'], '%Y/%m/%d')
        salary = int(request.form['salary'])
        if not Position.query.get(position_id):
            return make_response("invalid_position_id", 400)
        if not Department.query.get(department_id):
            return make_response('invalid_department_id', 400)
        employee = Employee.query.get(employee_id)
        if not employee:
            return make_response('invalid_employee_id', 400)
        employee.salary = salary
        employee.birthday = birthday
        employee.department_id = department_id
        employee.position_id = position_id
        db.session.commit()  # pylint: disable=E1101
        return make_response(employee_schema.jsonify(employee), 200)

    def delete(self, employee_id):  # pylint: disable=R0201
        """
        delete method for employee table
        """
        employee = Employee.query.get(employee_id)
        user = User.uery.get(employee_id)
        if employee:
            user.isEmployee = False
            db.session.delete(employee)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            return make_response(employee_schema.jsonify(employee), 200)
        return make_response("employee_not_found", 404)
