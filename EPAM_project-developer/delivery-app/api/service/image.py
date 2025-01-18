"""
CRUD operations for image table file
"""
import logging

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
            logging.info('Getting image by id started')
            image = Image.query.get(image_id)
            if image:
                logging.info('Image successfully found')
                return make_response(image_schema.jsonify(image), 200)
            logging.info('Getting image by id failed: image not found')
            return make_response("image_not_found", 404)
        # get all
        logging.info('Getting all images started')
        all_images = Image.query.all()
        result = images_schema.dump(all_images)
        logging.info('All images successfully got')
        return make_response(jsonify(result), 200)

    def post(self):  # pylint: disable=R0201, R0911
        """
        create method for image table
        """
        logging.info('Creation new image started')
        if request.form["img"] == "None":
            img = None
        else:
            img = request.form["img"]
        name = request.form["name"]
        mimetype = request.form["mimetype"]
        new_image = Image(img=img,
                     name=name,
                     mimetype=mimetype)
        db.session.add(new_image)  # pylint: disable=E1101
        db.session.commit()  # pylint: disable=E1101
        logging.info('Creation new image succeed')
        return make_response(image_schema.jsonify(new_image), 200)

    def put(self, image_id):  # pylint: disable=R0201
        """
        method tht updates image by id
        """
        logging.info('Update image started')
        image = Image.query.get(image_id)
        if image:
            if request.form["img"] == "None":
                image.img = None
            else:
                image.img = request.form["img"]
            image.name = request.form["name"]
            image.mimetype = request.form["mimetype"]
            db.session.commit()  # pylint: disable=E1101
            logging.info('Update image succeed')
            return make_response(image_schema.jsonify(image), 200)
        logging.info('Update image failed: image not found')
        return make_response("image_not_found", 404)

    def delete(self, image_id):  # pylint: disable=R0201
        """
        delete method for image table
        """
        logging.info('Deletion image started')
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)  # pylint: disable=E1101
            db.session.commit()  # pylint: disable=E1101
            logging.info('Deletion image succeed')
            return make_response(image_schema.jsonify(image), 200)
        logging.info('Deletion image fail: image not found')
        return make_response("image_not_found", 404)
