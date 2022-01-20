"""
views for signed in personnel officer user
"""
import re
import datetime
import logging
import requests
from flask_restful import Resource
from flask import render_template, make_response, request, redirect, session
from flask_login import login_required
from api.models import Employee  # pylint: disable=import-error


def department_avg_salary(department_id):
    """
    :param department_id
    :return: average salary of department
    """
    employees = Employee.query.filter_by(department_id=department_id)
    average_salary = 0
    count = 0
    for employee in employees:
        average_salary += employee.salary
        count += 1
    if count > 0:
        average_salary /= count
    return average_salary


class Departments(Resource):
    """
    methods for personnel officer departments page
    """
    @login_required
    def get(self):  # pylint: disable=R0201
        """
        get method for personnel officer departments page
        """
        logging.info("personnel officer departments page")
        if session.get('position') and session.get('position') == 'personnel officer':
            all_departments = requests.get(f'http://{request.host}/department').json()
            departments = []
            totally_avg = 0
            for department in all_departments:
                average_salary = department_avg_salary(department["id"])
                totally_avg += average_salary
                department_form = {"id": department["id"],
                                   "name": department["name"],
                                   "city": department["city"],
                                   "address": department["address"],
                                   "average salary": average_salary
                                   }
                departments.append(department_form)
            totally_avg /= len(departments)
            return make_response(render_template("personnel_officer/departments.html",
                                                 departments=departments,
                                                 totally_avg=totally_avg))
        logging.info("user is not personnel officer")
        logging.info("redirect to sign in page")
        return redirect("/sign_in")


class OneDepartment(Resource):
    """
    methods for personnel officer department page
    """

    @login_required
    def get(self, department_id):  # pylint: disable=R0201
        """
        get method for personnel officer department page
        """
        logging.info("personnel officer one department page")
        if session.get('position') and session.get('position') == 'personnel officer':
            request_department = requests.get(f'http://{request.host}/department/{department_id}')
            if request_department.status_code != 200:
                logging.info("department not found redirect to error page")
                return make_response(render_template("error.html",
                                                     base_tmp="personnel_officer/base.html",
                                                     text=request_department.text,
                                                     status_code=request_department.status_code))
            request_department = request_department.json()
            average_salary = department_avg_salary(request_department["id"])
            department = {"id": request_department["id"],
                          "name": request_department["name"],
                          "city": request_department["city"],
                          "address": request_department["address"],
                          "average salary": average_salary
                          }
            employees_request = Employee.query.filter_by(department_id=request_department["id"])
            employees = []
            for employee in employees_request:
                user = requests.get(f'http://{request.host}/user/{employee.id}').json()
                position = requests.get(
                    f'http://{request.host}/position/{employee.position_id}'
                ).json()
                employee_form = {
                    "id": user["id"],
                    "surname": user["surname"],
                    "name": user["name"],
                    "position": position["position_name"],
                    "birthday": employee.birthday,
                    "salary": employee.salary
                }
                employees.append(employee_form)
            return make_response(render_template("personnel_officer/department.html",
                                                 department=department,
                                                 employees=employees), 200)
        logging.info("user is not personnel officer")
        logging.info("redirect to sign in page")
        return redirect("/sign_in")


class Employees(Resource):
    """
    methods for personnel officer employees page
    """
    @login_required
    def get(self):  # pylint: disable=R0201
        """
        get method for personnel officer employees page
        """
        logging.info("personnel officer employees page")
        if session.get('position') and session.get('position') == 'personnel officer':
            all_employees = requests.get(f'http://{request.host}/employee').json()
            employees = []
            for employee in all_employees:
                user = requests.get(f'http://{request.host}/user/{employee["id"]}').json()
                position = requests.get(
                    f'http://{request.host}/position/{employee["position_id"]}'
                ).json()
                employee_form = {
                    "id": user["id"],
                    "surname": user["surname"],
                    "name": user["name"],
                    "position": position["position_name"],
                    "birthday": employee["birthday"],
                    "salary": employee["salary"],
                    "department_id": employee["department_id"]
                }
                employees.append(employee_form)
            return make_response(render_template("personnel_officer/employees.html",
                                                 employees=employees), 200)
        logging.info("user is not personnel officer")
        logging.info("redirect to sign in page")
        return redirect("/sign_in")

    @login_required
    def post(self):  # pylint: disable=R0201
        """
        filter
        """
        logging.info("personnel officer employee page filtered by date")
        if session.get('position') and session.get('position') == 'personnel officer':
            regex_1 = r'[0-9]{4}/[0-9]{2}/[0-9]{2}'
            regex_2 = r'[0-9]{4}/[0-9]{2}/[0-9]{2}:[0-9]{4}/[0-9]{2}/[0-9]{2}'
            dateline = request.form.get("input")
            if re.fullmatch(regex_1, str(dateline)):
                birthday = datetime.datetime.strptime(dateline, '%Y/%m/%d')
                employees_request = Employee.query.filter_by(birthday=birthday)
                employees = []
                for employee in employees_request:
                    user = requests.get(f'http://{request.host}/user/{employee.id}').json()
                    position = requests.get(
                        f'http://{request.host}/position/{employee.position_id}'
                    ).json()
                    employee_form = {
                        "id": user["id"],
                        "surname": user["surname"],
                        "name": user["name"],
                        "position": position["position_name"],
                        "birthday": employee.birthday,
                        "salary": employee.salary,
                        "department_id": employee.department_id
                    }
                    employees.append(employee_form)
                return make_response(render_template("personnel_officer/employees.html",
                                                     employees=employees), 200)
            elif re.fullmatch(regex_2, str(dateline)):
                date_1 = datetime.datetime.strptime(dateline[:10], '%Y/%m/%d')
                date_2 = datetime.datetime.strptime(dateline[11:], '%Y/%m/%d')
                employees_request = Employee.query.filter(Employee.birthday >= date_1
                                                          ).filter(Employee.birthday <= date_2)
                employees = []
                for employee in employees_request:
                    user = requests.get(f'http://{request.host}/user/{employee.id}').json()
                    position = requests.get(
                        f'http://{request.host}/position/{employee.position_id}'
                    ).json()
                    employee_form = {
                        "id": user["id"],
                        "surname": user["surname"],
                        "name": user["name"],
                        "position": position["position_name"],
                        "birthday": employee.birthday,
                        "salary": employee.salary,
                        "department_id": employee.department_id
                    }
                    employees.append(employee_form)
                return make_response(render_template("personnel_officer/employees.html",
                                                     employees=employees), 200)

            return redirect("/personnel_officer/employee")
        logging.info("user is not personnel officer")
        logging.info("redirect to sign in page")
        return redirect("/sign_in")


class OneEmployee(Resource):
    """
    methods for personnel officer one employee page
    """
    @login_required
    def get(self, employee_id):  # pylint: disable=R0201
        """
        get method for personnel officer one employee page
        """
        logging.info("personnel officer employees page")
        if session.get('position') and session.get('position') == 'personnel officer':
            employee_request = requests.get(f'http://{request.host}/employee/{employee_id}').json()
            user = requests.get(f'http://{request.host}/user/{employee_id}').json()
            position = requests.get(
                f'http://{request.host}/position/{employee_request["position_id"]}'
            ).json()
            employee = {
                "surname": user["surname"],
                "name": user["name"],
                "position": position["position_name"],
                "birthday": employee_request["birthday"],
                "salary": employee_request["salary"],
                "department_id": employee_request["department_id"]
            }
            request_department = requests.get(
                f'http://{request.host}/department/{employee["department_id"]}')
            request_department = request_department.json()
            average_salary = department_avg_salary(request_department["id"])
            department = {"id": request_department["id"],
                          "name": request_department["name"],
                          "city": request_department["city"],
                          "address": request_department["address"],
                          "average_salary": average_salary
                          }
            return make_response(render_template("personnel_officer/employee.html",
                                                 employee=employee,
                                                 department=department), 200)
        logging.info("user is not personnel officer")
        logging.info("redirect to sign in page")
        return redirect("/sign_in")
