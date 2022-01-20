"""
Tests
"""
import unittest
import flask_sqlalchemy

import api  # pylint: disable=import-error, C0413, no-name-in-module
from api import create_db  # pylint: disable=import-error, C0413, no-name-in-module
from api.rest.main import main  # pylint: disable=import-error, C0413, no-name-in-module
from api.rest.authorization import \
    authorization  # pylint: disable=import-error, C0413, no-name-in-module
from api.rest.personnel_officer import \
    personnel_officer  # pylint: disable=import-error, C0413, no-name-in-module

SETUP_DONE = False


class FlaskrTestCase(unittest.TestCase):  # pylint: disable=R0904
    """
    TESTS
    """

    def setUp(self):
        if create_db.is_database_exist("travis_test_db", passwd=""):
            create_db.delete_db("travis_test_db", passwd="")
        create_db.create_test_db(passwd="")
        global SETUP_DONE  # pylint: disable=W0603
        if not SETUP_DONE:
            SETUP_DONE = True
            api.app.config[
                'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/travis_test_db'
            api.app.config['TESTING'] = True
            db = flask_sqlalchemy.SQLAlchemy(api.app)  # pylint: disable=C0103, W0612

        from api.models import Position, User, Department, Employee, Image, DishCategory, Dish, \
            Status, Delivery, OrderedDish  # pylint: disable=import-error, C0413, wrong-import-position, W0614
        api.db.create_all()
        create_db.fill_db("travis_test_db", passwd="")
        self.app = api.app.test_client()

    def tearDown(self):
        create_db.delete_db("travis_test_db", passwd="")

    def test_position_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/position", data={"position_name": "position_name"})
        assert result.status_code == 200

    def test_position_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/position/1")
        assert result.status_code, result.get_json() == (200, dict(id=1, position_name="courier"))

    def test_position_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/position')
        assert result.status_code == 200

    def test_position_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/position/1")
        assert result.status_code == 200

    def test_position_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/position/1", data={"position_name": "position_name"})
        assert result.status_code == 200

    def test_department_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/department", data={"name": "name",
                                                    "city": "city",
                                                    "address": "address"})
        assert result.status_code == 200

    def test_department_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/department/1")
        assert result.status_code == 200

    def test_department_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/department')
        assert result.status_code == 200

    def test_department_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/department/1")
        assert result.status_code == 200

    def test_department_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/department/1", data={"name": "name",
                                                     "city": "city",
                                                     "address": "address"})
        assert result.status_code == 200

    def test_user_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/user", data={"email": "mail@gmail.com",
                                              "password": "password",
                                              "surname": "surname",
                                              "name": "name",
                                              "phoneNumber": "0980000000"})
        assert result.status_code == 200

    def test_user_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/user/1")
        assert result.status_code == 200

    def test_user_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/user')
        assert result.status_code == 200

    def test_user_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/user/1")
        assert result.status_code == 200

    def test_user_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/user/1", data={"email": "mail@gmail.com",
                                               "password": "password",
                                               "surname": "surname",
                                               "name": "name",
                                               "phoneNumber": "0980000000"})
        assert result.status_code == 200

    def test_employee_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/employee", data={"id": 1,
                                                  "position_id": 1,
                                                  "department_id": 1,
                                                  "birthday": "1991/09/8",
                                                  "salary": 1})
        assert result.status_code == 200

    def test_employee_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/employee/2")
        assert result.status_code == 200

    def test_employee_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/employee')
        assert result.status_code == 200

    def test_employee_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/employee/2")
        assert result.status_code == 200

    def test_employee_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/employee/2", data={"position_id": 1,
                                                   "department_id": 1,
                                                   "birthday": "1991/09/8",
                                                   "salary": 1})
        assert result.status_code == 200

    def test_image_create_succeed(self):  # pylint: disable=C0116
        # image = create_db.convertToBinaryData("../static/images/test.png")
        result = self.app.post("/image", data={"img": "None",
                                               "name": "name",
                                               "mimetype": "png"})
        assert result.status_code == 200

    def test_image_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/image/1")
        assert result.status_code == 200

    def test_image_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/image')
        assert result.status_code == 200

    def test_image_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/image/1")
        assert result.status_code == 200

    def test_image_update_succeed(self):  # pylint: disable=C0116
        # image = create_db.convertToBinaryData("../static/images/test.png")
        result = self.app.put("/image/1", data={"img": "None",
                                                "name": "name",
                                                "mimetype": "png"})
        assert result.status_code == 200

    def test_dish_category_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/dish_category", data={"category_name": "category"})
        assert result.status_code == 200

    def test_dish_category_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/dish_category/1")
        assert result.status_code == 200

    def test_dish_category_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/dish_category')
        assert result.status_code == 200

    def test_dish_category_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/dish_category/1")
        assert result.status_code == 200

    def test_dish_category_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/dish_category/1", data={"category_name": "category"})
        assert result.status_code == 200

    def test_dish_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/dish", data={"category_id": 1,
                                              "dish_name": "name",
                                              "cost_price": 50,
                                              "value_added": 50,
                                              "image_id": 1,
                                              "description": "description"})
        assert result.status_code == 200

    def test_dish_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/dish/1")
        assert result.status_code == 200

    def test_dish_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/dish')
        assert result.status_code == 200

    def test_dish_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/dish/1")
        assert result.status_code == 200

    def test_dish_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/dish/1", data={"category_id": 1,
                                               "dish_name": "name",
                                               "cost_price": 50,
                                               "value_added": 50,
                                               "image_id": 1,
                                               "description": "description"})
        assert result.status_code == 200

    def test_status_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/status", data={"status_name": "status"})
        assert result.status_code == 200

    def test_status_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/status/1")
        assert result.status_code == 200

    def test_status_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/status')
        assert result.status_code == 200

    def test_status_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/status/1")
        assert result.status_code == 200

    def test_status_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/status/1", data={"status_name": "status"})
        assert result.status_code == 200

    def test_delivery_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/delivery", data={"department_id": 1,
                                                  "customer_id": 1,
                                                  "courier_id": 2,
                                                  "date": "2022/01/1",
                                                  "customer_address": "customer_address",
                                                  "status_id": 1})
        assert result.status_code == 200

    def test_delivery_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/delivery/1")
        assert result.status_code == 200

    def test_delivery_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/delivery')
        assert result.status_code == 200

    def test_delivery_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/delivery/1")
        assert result.status_code == 200

    def test_delivery_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/delivery/1", data={"department_id": 1,
                                                   "customer_id": 1,
                                                   "courier_id": 2,
                                                   "date": "2022/01/01",
                                                   "customer_address": "customer_address",
                                                   "status_id": 1})
        assert result.status_code == 200

    def test_ordered_dish_create_succeed(self):  # pylint: disable=C0116
        result = self.app.post("/ordered_dish", data={"delivery_id": 1,
                                                      "dish_id": 1,
                                                      "status_id": 1})
        assert result.status_code == 200

    def test_ordered_dish_get_by_id_succeed(self):  # pylint: disable=C0116
        result = self.app.get("/ordered_dish/1")
        assert result.status_code == 200

    def test_ordered_dish_get_all_succeed(self):  # pylint: disable=C0116
        result = self.app.get('/ordered_dish')
        assert result.status_code == 200

    def test_ordered_dish_delete_succeed(self):  # pylint: disable=C0116
        result = self.app.delete("/ordered_dish/1")
        assert result.status_code == 200

    def test_ordered_dish_update_succeed(self):  # pylint: disable=C0116
        result = self.app.put("/ordered_dish/1", data={"delivery_id": 1,
                                                       "dish_id": 1,
                                                       "status_id": 1})
        assert result.status_code == 200

    def test_sign_in(self):  # pylint: disable=C0116
        result = self.app.get("/sign_in")
        assert result.status_code == 200

    def test_sign_in_post(self):  # pylint: disable=C0116
        result = self.app.post("/sign_in", data={"email": "email",
                                                 "password": "password"})
        assert result.status_code == 200

    def test_sign_out(self):  # pylint: disable=C0116
        result = self.app.get("sign_out")
        assert result.status_code == 200

    def test_index(self):  # pylint: disable=C0116
        result = self.app.get("/")
        assert result.status_code == 200

    def test_personnel_officer_department(self):  # pylint: disable=C0116
        result = self.app.get("personnel_officer/department")
        assert result.status_code == 200

    def test_personnel_officer_department_1(self):  # pylint: disable=C0116
        result = self.app.get("personnel_officer/department/1")
        assert result.status_code == 200

    def test_personnel_officer_employees(self):  # pylint: disable=C0116
        result = self.app.get("personnel_officer/employee")
        assert result.status_code == 200

    def test_personnel_officer_employee(self):  # pylint: disable=C0116
        result = self.app.get("personnel_officer/employee/2")
        assert result.status_code == 200

    def test_personnel_officer_employees_post(self):  # pylint: disable=C0116
        result = self.app.post("personnel_officer/employee", data={"input":"2002/01/01"})
        assert result.status_code == 200


if __name__ == '__main__':
    unittest.main()
