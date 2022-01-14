"""
start application
"""
import requests
from flask import Flask, jsonify, request, render_template, make_response, Response
import flask_sqlalchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_wtf import FlaskForm
from wtforms import StringField
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Fsmnl2002@localhost/delivery_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = flask_sqlalchemy.SQLAlchemy(app)
ma = Marshmallow(app)


class PositionSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for position table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for position table schema
        """
        fields = ('id',
                  'position_name')


class UserSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for user table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for user table schema
        """
        fields = ('id',
                  'email',
                  'password',
                  'name',
                  'surname',
                  'phoneNumber',
                  'isEmployee')


class EmployeeSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for employee table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for employee table schema
        """
        fields = ('id',
                  'position_id',
                  'department_id',
                  'birthday',
                  'salary')


class DepartmentSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for department table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for department table schema
        """
        fields = ('id',
                  'name',
                  'city',
                  'address')


class ImageSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for image table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for image table schema
        """
        fields = ('id',
                  'img',
                  'name',
                  'mimetype')


class DishCategorySchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for dish category table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for dish category table schema
        """
        fields = ('id',
                  'category_name')


class DishSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for dish table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for dish table schema
        """
        fields = ('id',
                  'category_id',
                  'dish_name',
                  'cost_price',
                  'value_added',
                  'image_id',
                  'description')


class StatusSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for status table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for status table schema
        """
        fields = ('id',
                  'status_name')


class DeliverySchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for delivery table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for delivery table schema
        """
        fields = ('id',
                  'department_id',
                  'customer_id',
                  'courier_id',
                  'date',
                  'customer_address',
                  'status_id')


class OrderSchema(ma.Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for order table
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta for order table schema
        """
        fields = ('id',
                  'delivery_id',
                  'dish_id',
                  'status_id')


class PositionForm(FlaskForm):
    position_name = StringField("position_name")


from api.service.position import PositionCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.ordered_dish import OrderedDishCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.image import ImageCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.dish import DishCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.user import UserCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.dish_category import DishCategoryCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.department import DepartmentCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.employee import EmployeeCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.status import StatusCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.service.delivery import DeliveryCRUD  # pylint: disable=import-error, C0413, no-name-in-module
from api.models import Image  # pylint: disable=import-error, C0413, no-name-in-module

api.add_resource(PositionCRUD, '/position', '/position/<int:position_id>')
api.add_resource(OrderedDishCRUD, '/ordered_dish', '/ordered_dish/<int:order_id>')
api.add_resource(ImageCRUD, '/image', '/image/<int:image_id>')
api.add_resource(DishCRUD, '/dish', '/dish/<int:dish_id>')
api.add_resource(UserCRUD, '/user', '/user/<int:user_id>')
api.add_resource(DishCategoryCRUD, '/dish_category', '/dish_category/<int:dish_category_id>')
api.add_resource(DepartmentCRUD, '/department', '/department/<int:department_id>')
api.add_resource(EmployeeCRUD, '/employee', '/employee/<int:employee_id>')
api.add_resource(StatusCRUD, '/status', '/status/<int:status_id>')
api.add_resource(DeliveryCRUD, '/delivery', '/delivery/<int:delivery_id>')
positions_schema = PositionSchema(many=True)


@app.route("/")
def index():
    # position_crud = PositionCRUD()
    # position = requests.get('http://127.0.0.1:5000/position/1')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Image(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return 'Img Uploaded!', 200


@app.route('/<int:id>')
def get_img(id):
    # img = Image.query.filter_by(id=id).first()
    # if not img:
    #     return 'Img Not Found!', 404
    #
    # return Response(img.img, mimetype=img.mimetype)
    # position = requests.post(f'http://127.0.0.1:5000/position', data={"position_name":"position"})
    image =  requests.get(f'http://127.0.0.1:5000/image/{id}')
    return image.content
