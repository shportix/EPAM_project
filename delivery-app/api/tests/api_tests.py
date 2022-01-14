import json
import os
import datetime
import unittest
import tempfile
import flask_sqlalchemy
import requests

import api
from api import create_db

setup_done = False


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        if create_db.is_database_exist("travis_test_db", passwd="Fsmnl2002"):
            create_db.delete_db("travis_test_db", passwd="Fsmnl2002")
        create_db.create_test_db(passwd="Fsmnl2002")
        global setup_done
        if not setup_done:
            setup_done = True
            api.app.config[
                'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Fsmnl2002@localhost/travis_test_db'
            api.app.config['TESTING'] = True
            db = flask_sqlalchemy.SQLAlchemy(api.app)
        from api.models import Position, User, Department, Employee, Image, DishCategory, Dish, \
            Status, Delivery, OrderedDish
        api.db.create_all()
        create_db.fill_db("travis_test_db", passwd="Fsmnl2002")
        self.app = api.app.test_client()

    def tearDown(self):
        create_db.delete_db("travis_test_db", passwd="Fsmnl2002")

    def test_position_create_succeed(self):
        result = self.app.post("/position", data={"position_name": "position_name"})
        assert result.status_code == 200

    def test_position_get_by_id_succeed(self):
        result = self.app.get("/position/1")
        assert result.status_code, result.get_json() == (200, dict(id=1, position_name="courier"))

    def test_position_get_all_succeed(self):
        result = self.app.get('/positions')
        assert result.status_code == 200

    def test_position_delete_succeed(self):
        result = self.app.delete("/position/1")
        assert result.status_code == 200

    def test_position_update_succeed(self):
        result = self.app.put("/position/1", data={"position_name": "position_name"})
        assert result.status_code == 200

    def test_department_create_succeed(self):
        result = self.app.post("/department", data={"name": "name",
                                                    "city": "city",
                                                    "address": "address"})
        assert result.status_code == 200

    def test_department_get_by_id_succeed(self):
        result = self.app.get("/department/1")
        assert result.status_code == 200

    def test_department_get_all_succeed(self):
        result = self.app.get('/department')
        assert result.status_code == 200

    def test_department_delete_succeed(self):
        result = self.app.delete("/department/1")
        assert result.status_code == 200

    def test_department_update_succeed(self):
        result = self.app.put("/department/1", data={"name": "name",
                                                     "city": "city",
                                                     "address": "address"})
        assert result.status_code == 200

    def test_user_create_succeed(self):
        result = self.app.post("/user", data={"email": "mail@gmail.com",
                                              "password": "password",
                                              "surname": "surname",
                                              "name": "name",
                                              "phoneNumber": "0980000000"})
        assert result.status_code == 200

    def test_user_get_by_id_succeed(self):
        result = self.app.get("/user/1")
        assert result.status_code == 200

    def test_user_get_all_succeed(self):
        result = self.app.get('/user')
        assert result.status_code == 200

    def test_user_delete_succeed(self):
        result = self.app.delete("/user/1")
        assert result.status_code == 200

    def test_user_update_succeed(self):
        result = self.app.put("/user/1", data={"email": "mail@gmail.com",
                                               "password": "password",
                                               "surname": "surname",
                                               "name": "name",
                                               "phoneNumber": "0980000000"})
        assert result.status_code == 200

    def test_employee_create_succeed(self):
        result = self.app.post("/employee", data={"id": 1,
                                                  "position_id": 1,
                                                  "department_id": 1,
                                                  "birthday": datetime.datetime.strptime(
                                                      "1991/09/8", '%Y/%m/%d'),
                                                  "salary": 1})
        assert result.status_code == 200

    def test_employee_get_by_id_succeed(self):
        result = self.app.get("/employee/1")
        assert result.status_code == 200

    def test_employee_get_all_succeed(self):
        result = self.app.get('/employee')
        assert result.status_code == 200

    def test_employee_delete_succeed(self):
        result = self.app.delete("/employee/1")
        assert result.status_code == 200

    def test_employee_update_succeed(self):
        result = self.app.put("/employee/1", data={"position_id": 1,
                                                   "department_id": 1,
                                                   "birthday": datetime.datetime.strptime(
                                                       "1991/09/8", '%Y/%m/%d'),
                                                   "salary": 1})
        assert result.status_code == 200

    def test_image_create_succeed(self):
        image = create_db.convertToBinaryData("../static/images/test.png")
        result = self.app.post("/image", data={"img": image,
                                               "name": "name",
                                               "mimetype": "png"})
        assert result.status_code == 200

    def test_image_get_by_id_succeed(self):
        result = self.app.get("/image/1")
        assert result.status_code == 200

    def test_image_get_all_succeed(self):
        result = self.app.get('/image')
        assert result.status_code == 200

    def test_image_delete_succeed(self):
        result = self.app.delete("/image/1")
        assert result.status_code == 200

    def test_image_update_succeed(self):
        image = create_db.convertToBinaryData("../static/images/test.png")
        result = self.app.put("/image/1", data={"img": image,
                                                "name": "name",
                                                "mimetype": "png"})
        assert result.status_code == 200

    def test_dish_category_create_succeed(self):
        result = self.app.post("/dish_category", data={"category_name": "category"})
        assert result.status_code == 200

    def test_dish_category_get_by_id_succeed(self):
        result = self.app.get("/dish_category/1")
        assert result.status_code == 200

    def test_dish_category_get_all_succeed(self):
        result = self.app.get('/dish_category')
        assert result.status_code == 200

    def test_dish_category_delete_succeed(self):
        result = self.app.delete("/dish_category/1")
        assert result.status_code == 200

    def test_dish_category_update_succeed(self):
        result = self.app.put("/dish_category/1", data={"category_name": "category"})
        assert result.status_code == 200

    def test_dish_create_succeed(self):
        result = self.app.post("/dish", data={"category_id": 1,
                                              "dish_name": "name",
                                              "cost_price": 50,
                                              "value_added": 50,
                                              "image_id": 1,
                                              "description": "description"})
        assert result.status_code == 200

    def test_dish_get_by_id_succeed(self):
        result = self.app.get("/dish/1")
        assert result.status_code == 200

    def test_dish_get_all_succeed(self):
        result = self.app.get('/dish')
        assert result.status_code == 200

    def test_dish_delete_succeed(self):
        result = self.app.delete("/dish/1")
        assert result.status_code == 200

    def test_dish_update_succeed(self):
        result = self.app.put("/dish/1", data={"category_id": 1,
                                               "dish_name": "name",
                                               "cost_price": 50,
                                               "value_added": 50,
                                               "image_id": 1,
                                               "description": "description"})
        assert result.status_code == 200

    def test_status_create_succeed(self):
        result = self.app.post("/status", data={"status_name": "status"})
        assert result.status_code == 200

    def test_status_get_by_id_succeed(self):
        result = self.app.get("/status/1")
        assert result.status_code == 200

    def test_status_get_all_succeed(self):
        result = self.app.get('/status')
        assert result.status_code == 200

    def test_status_delete_succeed(self):
        result = self.app.delete("/status/1")
        assert result.status_code == 200

    def test_status_update_succeed(self):
        result = self.app.put("/status/1", data={"status_name": "status"})
        assert result.status_code == 200

    def test_delivery_create_succeed(self):
        result = self.app.post("/delivery", data={"department_id": 1,
                                                  "customer_id": 1,
                                                  "courier_id": 2,
                                                  "date": datetime.datetime.strptime("2022/01/1",
                                                                                     '%Y/%m/%d'),
                                                  "customer_address": "customer_address",
                                                  "status_id": 1})
        assert result.status_code == 200

    def test_delivery_get_by_id_succeed(self):
        result = self.app.get("/delivery/1")
        assert result.status_code == 200

    def test_delivery_get_all_succeed(self):
        result = self.app.get('/delivery')
        assert result.status_code == 200

    def test_delivery_delete_succeed(self):
        result = self.app.delete("/delivery/1")
        assert result.status_code == 200

    def test_delivery_update_succeed(self):
        result = self.app.put("/delivery/1", data={"department_id": 1,
                                                   "customer_id": 1,
                                                   "courier_id": 2,
                                                   "date": datetime.datetime.strptime("2022/01/1",
                                                                                      '%Y/%m/%d'),
                                                   "customer_address": "customer_address",
                                                   "status_id": 1})
        assert result.status_code == 200

    def test_ordered_dish_create_succeed(self):
        result = self.app.post("/ordered_dish", data={"delivery_id": 1,
                                                      "dish_id": 1,
                                                      "status_id": 1})
        assert result.status_code == 200

    def test_ordered_dish_get_by_id_succeed(self):
        result = self.app.get("/ordered_dish/1")
        assert result.status_code == 200

    def test_ordered_dish_get_all_succeed(self):
        result = self.app.get('/ordered_dish')
        assert result.status_code == 200

    def test_ordered_dish_delete_succeed(self):
        result = self.app.delete("/ordered_dish/1")
        assert result.status_code == 200

    def test_ordered_dish_update_succeed(self):
        result = self.app.put("/ordered_dish/1", data={"delivery_id": 1,
                                                       "dish_id": 1,
                                                       "status_id": 1})
        assert result.status_code == 200


if __name__ == '__main__':
    unittest.main()
