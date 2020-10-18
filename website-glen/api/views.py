from flask import Blueprint, jsonify, request
from . import db
from .models import ImageFile
import os

main = Blueprint('main', __name__)

@main.route('/save_images', methods=['POST'])
def save_images():
    file_data = request.get_json()

    new_image_file = ImageFile(userID=file_data['userID'], filepath=file_data['filepath'])
    #validate file

    #save image to local storage 
    #os.save(new_image_file)

    #email file to user

    db.session.add(new_image_file)
    db.session.commit()

    #return success response to front end
    return 'Done', 201

@main.route('/images')
def images():
    image_list = ImageFile.query.all()
    images = []

    for image_data in image_list:
        images.append({"userID" : image_data.userID, "filepath" : image_data.filepath})

    return jsonify({'images' : images})

#after request [POST] requests only
#validate file exists, if it does, delete file