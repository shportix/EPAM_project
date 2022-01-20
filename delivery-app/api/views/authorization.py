"""
views for authorization functions
"""
import logging
from flask_restful import Resource
from flask import render_template, make_response, request, redirect, session
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from api.models import User, Employee, Position  # pylint: disable=import-error


class SignIn(Resource):
    """
    methods for sign in
    """
    def get(self):  # pylint: disable=R0201
        """
        sign in get method
        """
        logging.info("sign in page")
        if current_user.is_authenticated:
            logging.info("user is authenticated")
            if not current_user.isEmployee:
                name = "" if current_user.name is None else current_user.name
                surname = "" if current_user.surname is None else current_user.surname
                phone_number = "" if current_user.phoneNumber is None else current_user.phoneNumber
                logging.info("redirect to customer profile page")
                return make_response(render_template("customer/profile.html",
                                                     name=name,
                                                     surname=surname,
                                                     phoneNumber=phone_number),200)
            employee = Employee.query.get(current_user.id)
            position = Position.query.get(employee.position_id).position_name
            session['position'] = position
            if position == 'personnel officer':
                logging.info("redirect to personnel officer departments page")
                return redirect('/personnel_officer/department')
        return make_response(render_template("authorization/sign_in.html"), 200)

    def post(self):  # pylint: disable=R0201
        """
        sign in post method
        """
        logging.info("user sign in")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
        return redirect("/sign_in")


class SignOut(Resource):
    """
    sign out methods
    """
    def get(self):  # pylint: disable=R0201
        """
        sign out method
        """
        logging.info("user sign out")
        if current_user.is_authenticated:
            logout_user()
            if session.get('employee'):
                session.pop('employee')
            if session.get('position'):
                session.pop('position')
        return redirect("/")
