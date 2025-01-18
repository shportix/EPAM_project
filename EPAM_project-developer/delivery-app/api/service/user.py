"""
CRUD operations for user table file
"""
import logging
import re
from flask import jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from api.models import User  # pylint: disable=import-error
from api import db, UserSchema  # pylint: disable=import-error


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def validate_email(email):
    """
    email validation function
    """
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex_email, email)


def validate_phone_number(phone_number):
    """
    phone number validation function
    """
    regex_phone = r'([0-9]{10})'
    return re.fullmatch(regex_phone, phone_number)


class UserCRUD(Resource):
    """
    CRUD operations for user table
    """

    def get(self, user_id=None):  # pylint: disable=R0201
        """
        read method for user table
        """
        if user_id is not None:
            # get by id
            logging.info('Getting user by id started')
            user = User.query.get(user_id)
            if user:
                logging.info('Delivery successfully found')
                return make_response(user_schema.jsonify(user), 200)
            logging.info('Getting user by id failed: user not found')
            return make_response("user_not_found", 404)
        # get all
        logging.info('Getting all users started')
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        logging.info('All users successfully got')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for user table
        """
        logging.info('Creation new user started')
        email = request.form['email']
        if len(request.form['password']) < 7:
            logging.info('Creation user failed: password length < 7')
            return make_response("too_short_password", 400)
        password = generate_password_hash(request.form['password'])
        name = None if request.form['name'] == "" else request.form['name']
        surname = None if request.form['surname'] == "" else request.form['surname']
        phone_number = None if request.form['phoneNumber'] == "" else request.form['phoneNumber']
        if phone_number is not None:
            if not validate_phone_number(phone_number):
                logging.info('Creation user failed: invalid phone number')
                return make_response("Invalid_phone_number", 400)
        if not validate_email(email):
            logging.info('Creation user failed: invalid email')
            return make_response("invalid_email", 400)
        if User.query.filter_by(email=email).first():
            logging.info('Creation user failed: user with this email exist')
            return make_response('user_with_this_email_exist', 400)
        new_user = User(email=email,
                        password=password,
                        name=name,
                        surname=surname,
                        phoneNumber=phone_number,
                        isEmployee=False)
        db.session.add(new_user)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation user succeed')
        return make_response(user_schema.jsonify(new_user), 200)

    def put(self, user_id):  # pylint: disable=R0201
        """
        method tht updates user by id
        """
        logging.info('Update user started')
        user = User.query.get(user_id)
        if user:
            email = request.form['email']
            if len(request.form['password']) < 7:
                logging.info('Update user failed: password length < 7')
                return make_response("too_short_password", 400)
            password = generate_password_hash(request.form['password'])
            name = None if request.form['name'] == "" else request.form['name']
            surname = None if request.form['surname'] == "" else request.form['surname']
            phone_number = None if request.form['phoneNumber'] == "" else request.form['phoneNumber']
            if phone_number is not None:
                if not validate_phone_number(phone_number):
                    logging.info('Update user failed: invalid phone number')
                    return make_response("Invalid_phone_number", 400)
            if not validate_email(email):
                logging.info('Update user failed: invalid email')
                return make_response("invalid_email", 400)
            if User.query.filter_by(email=email).first():
                if User.query.filter_by(email=email).first() != user:
                    logging.info('Update user failed: user with this email exist')
                    return make_response('user_with_this_email_exist', 400)
            user.email = email
            user.password = password
            user.name = name
            user.surname = surname
            user.phoneNumber = phone_number

            db.session.commit()  # pylint: disable=E1101
            logging.info('Update user succeed')
            return make_response(user_schema.jsonify(user), 200)
        logging.info('Update user failed: user not found')
        return make_response("delivery_not_found", 404)



    def delete(self, user_id):  # pylint: disable=R0201
        """
        delete method for position table
        """
        logging.info('Deletion position started')
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion position succeed')
            return make_response(user_schema.jsonify(user), 200)
        logging.info('Deletion position fail: position not found')
        return make_response("position_not_found", 404)
