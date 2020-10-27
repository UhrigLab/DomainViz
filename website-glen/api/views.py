from flask import Blueprint, jsonify, request
from . import db
from .models import ImageFile
import os
import subprocess

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

@main.route('/partonefiles', methods=['POST'])
def partonefiles():
    # data comes in the format:
    # b'-----------------------------197130814939513389033381765664\r\nContent-Disposition: form-data; name="userID"; filename="XXXX.fa"\r\nContent-Type: application/octet-stream\r\n\r\nThese are the words I am writing.\r\n-----------------------------197130814939513389033381765664--\r\n'
    user_id = request.get_data()
    user_id = user_id.decode("utf-8")
    
    # remove the content not including the name sent by the front-end, which is the unique userID
    user_id = user_id.split(sep="name=\"")[1]
    user_id = user_id.split(sep="\"")[0]
    
    file_data = request.files[user_id]
    # TODO validate file
    file_path = 'api/tmp/' 
    file_data.save(os.path.abspath(file_path + file_data.filename))

    # call Pascals script for fasta files here
    call = "python3 api/propplot_pfamtest.py -id " + user_id + " -in " + file_path + file_data.filename + " -sf " + file_path + " -dbf api/dbs/"
    subprocess.call(call, shell=True)
    # TODO save pdf in local folder and save to database with user_id being the userID

    return 'Done', 201

@main.route('/parttwofiles', methods=['POST'])
def parttwofiles():
    data = request.get_data()
    print(data)
    return 'Done', 201
#after request [POST] requests only
#validate file exists, if it does, delete file