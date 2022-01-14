"""
CRUD operations for image table file
"""
from flask import jsonify, request, make_response
from flask_restful import Resource
from api.models import Image  # pylint: disable=import-error
from api import db, ImageSchema  # pylint: disable=import-error

images_schema = ImageSchema(many=True)
image_schema = ImageSchema()


class ImageCRUD(Resource):
    """
    CRUD operations for image table
    """
    def get(self, image_id=None):  # pylint: disable=R0201
        """
        read method for image table
        """
        if image_id is not None:
            # get by id
            image = Image.query.get(image_id)
            if image:
                return make_response(image_schema.jsonify(image), 200)
            return make_response("image_not_found", 404)
        # get all
        all_images = Image.query.all()
        result = images_schema.dump(all_images)
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for image table
        """
        img = request.form["img"]
        name = request.form["name"]
        mimetype = request.form["mimetype"]
        new_image = Image(img=img,
                     name=name,
                     mimetype=mimetype)
        db.session.add(new_image)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        return make_response(image_schema.jsonify(new_image), 200)

    def put(self, image_id):  # pylint: disable=R0201
        """
        method tht updates image by id
        """
        image = Image.query.get(image_id)
        if image:
            image.img = request.form["img"]
            image.name = request.form["name"]
            image.mimetype = request.form["mimetype"]
            db.session.commit()  # pylint: disable=E1101
            return make_response(image_schema.jsonify(image), 200)
        return make_response("image_not_found", 404)

    def delete(self, image_id):  # pylint: disable=R0201
        """
        delete method for image table
        """
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            return make_response(image_schema.jsonify(image), 200)
        return make_response("image_not_found", 404)
