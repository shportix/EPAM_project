import datetime
import mysql.connector
from werkzeug.security import generate_password_hash


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def create_db(name, host="localhost", user="root", passwd=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
    )

    my_cursor = mydb.cursor()

    my_cursor.execute(f"CREATE DATABASE {name}")


def create_test_db(host="localhost", user="root", passwd=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        auth_plugin='mysql_native_password'
    )

    my_cursor = mydb.cursor()

    my_cursor.execute("CREATE DATABASE travis_test_db")


def fill_positions(name, host="localhost", user="root", passwd=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=name
    )
    my_cursor = mydb.cursor()


def fill_db(name, host="localhost", user="root", passwd=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=name
    )

    my_cursor = mydb.cursor()

    add_position = f"INSERT INTO position (id, position_name) VALUES (%s,%s)"
    add_user = "INSERT INTO user (id, email, password, name, surname, phoneNumber, isEmployee) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    add_department = "INSERT INTO department " \
                     "(id, name, city, address) " \
                     "VALUES (%s,%s,%s,%s)"
    add_employee = "INSERT INTO employee " \
                   "(id,position_id, department_id, birthday, salary) " \
                   "VALUES (%s,%s,%s,%s,%s)"
    add_image = "INSERT INTO image " \
                "(id, img, name, mimetype) " \
                "VALUES (%s,%s,%s,%s)"
    add_dish_category = "INSERT INTO dish_category " \
                        "(id, category_name) " \
                        "VALUES (%s,%s)"
    add_dish = "INSERT INTO dish " \
               "(id, category_id,dish_name, cost_price, value_added, image_id, description) " \
               "VALUES (%s,%s,%s,%s,%s,%s,%s)"
    add_status = "INSERT INTO status " \
                 "(id, status_name) " \
                 "VALUES (%s,%s)"
    add_delivery = "INSERT INTO delivery " \
                   "(id, department_id,customer_id, courier_id, date, customer_address, status_id) " \
                   "VALUES (%s,%s,%s,%s,%s,%s,%s)"
    add_ordered_dish = "INSERT INTO ordered_dish " \
                       "(id, delivery_id,dish_id, status_id) " \
                       "VALUES (%s,%s,%s,%s)"

    my_cursor.execute(add_department, (1,
                                       "IT",
                                       "Kharkiv",
                                       "Sumska street 74"))
    my_cursor.execute(add_department, (2,
                                       None,
                                       "Kharkiv",
                                       "Sumska street 60"))

    my_cursor.execute(add_position, (1,
                                     "courier",))
    my_cursor.execute(add_position, (2,
                                     "admin",))
    my_cursor.execute(add_position, (3,
                                     "chef",))
    my_cursor.execute(add_position, (4,
                                     "personel_officer",))
    my_cursor.execute(add_position, (5,
                                     "cook",))

    my_cursor.execute(add_user, (1,
                                 "customer@gmil.com",
                                 generate_password_hash("password"),
                                 "customer_name",
                                 "customer_surname",
                                 "0980000000",
                                 False))
    my_cursor.execute(add_user, (2,
                                 "courier@gmil.com",
                                 generate_password_hash("password"),
                                 "courier_name",
                                 "courier_surname",
                                 "0980000000",
                                 True))
    my_cursor.execute(add_user, (3,
                                 "admin@gmil.com",
                                 generate_password_hash("password"),
                                 "admin_name",
                                 "admin_surname",
                                 "0980000000",
                                 True))
    my_cursor.execute(add_user, (4,
                                 "personel_officer@gmil.com",
                                 generate_password_hash("password"),
                                 "personel_officer_name",
                                 "personel_officer_surname",
                                 "0980000000",
                                 True))
    my_cursor.execute(add_user, (5,
                                 "chef@gmil.com",
                                 generate_password_hash("password"),
                                 "chef_name",
                                 "chef_surname",
                                 "0980000000",
                                 True))
    my_cursor.execute(add_user, (6,
                                 "cook@gmil.com",
                                 generate_password_hash("password"),
                                 "cook_name",
                                 "cook_surname",
                                 "0980000000",
                                 True))

    my_cursor.execute(add_employee, (2,
                                     1,
                                     2,
                                     datetime.datetime.strptime("2002/06/25", '%Y/%m/%d'),
                                     12000))
    my_cursor.execute(add_employee, (3,
                                     2,
                                     1,
                                     datetime.datetime.strptime("1998/06/19", '%Y/%m/%d'),
                                     20000))
    my_cursor.execute(add_employee, (4,
                                     3,
                                     2,
                                     datetime.datetime.strptime("1990/04/14", '%Y/%m/%d'),
                                     25000))
    my_cursor.execute(add_employee, (5,
                                     4,
                                     2,
                                     datetime.datetime.strptime("1991/09/8", '%Y/%m/%d'),
                                     25000))
    my_cursor.execute(add_employee, (6,
                                     5,
                                     2,
                                     datetime.datetime.strptime("2000/08/25", '%Y/%m/%d'),
                                     15000))

    image = convertToBinaryData(
        "../static/images/roll-kaliforniya.jpg")
    my_cursor.execute(add_image, (1,
                                  image,
                                  "roll-kaliforniya",
                                  "jpg"))
    image = convertToBinaryData(
        "../static/images/cheeseburger.jpeg")
    my_cursor.execute(add_image, (2,
                                  image,
                                  "cheeseburger",
                                  "jpeg"))

    my_cursor.execute(add_dish_category, (1,
                                          "Burgers",))
    my_cursor.execute(add_dish_category, (2,
                                          "Rolls",))

    my_cursor.execute(add_dish, (1,
                                 1,
                                 "cheeseburger",
                                 150,
                                 75,
                                 2,
                                 "this is a cheeseburger"))
    my_cursor.execute(add_dish, (2,
                                 2,
                                 "roll kaliforniya",
                                 200,
                                 200,
                                 1,
                                 "this is a roll kaliforniya"))

    my_cursor.execute(add_status, (1,
                                   "waiting for cooking",))
    my_cursor.execute(add_status, (2,
                                   "cooking",))
    my_cursor.execute(add_status, (3,
                                   "waiting for delivery",))
    my_cursor.execute(add_status, (4,
                                   "delivering",))
    my_cursor.execute(add_status, (5,
                                   "done",))

    my_cursor.execute(add_delivery, (1,
                                     2,
                                     1,
                                     2,
                                     datetime.datetime.strptime("2022/01/1", '%Y/%m/%d'),
                                     "customer_address",
                                     5))

    my_cursor.execute(add_ordered_dish, (1,
                                         1,
                                         1,
                                         5))
    my_cursor.execute(add_ordered_dish, (2,
                                         1,
                                         2,
                                         5))
    mydb.commit()
    mydb.close()


def delete_db(name, host="localhost", user="root", passwd=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
    )

    my_cursor = mydb.cursor()

    my_cursor.execute(f"DROP DATABASE {name}")


def is_database_exist(name, host="localhost", user="root", passwd=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
    )

    my_cursor = mydb.cursor()

    my_cursor.execute(f"SHOW DATABASES LIKE '{name}'")
    for row in my_cursor:
        return True
    return False
