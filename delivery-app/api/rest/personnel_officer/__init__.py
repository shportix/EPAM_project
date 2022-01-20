from flask import Blueprint
from flask_restful import Api
from api.views.personnel_officer import Departments, OneDepartment, Employees, OneEmployee

personnel_officer = Blueprint('personnel_officer', __name__)
api = Api(personnel_officer)

api.add_resource(Departments, "/department")
api.add_resource(OneDepartment, "/department/<int:department_id>")
api.add_resource(Employees, "/employee")
api.add_resource(OneEmployee, "/employee/<int:employee_id>")
