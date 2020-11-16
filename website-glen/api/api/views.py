from flask import Blueprint, jsonify, request, redirect
from flask.helpers import url_for
from api.__init__ import db
from api.models import PDFModel

import os, subprocess, base64, glob

main = Blueprint('main', __name__, static_folder="../build", static_url_path='/')
@main.route('/')
def index():
    return main.send_static_file('index.html')
@main.route('/api/images/<username>')
def images(username):
    print(username)
    result_id = username
    image_list = PDFModel.query.all()
    images = []

    for image_data in image_list:
        if image_data.resultID == result_id:
            b64_bytes = base64.b64encode(image_data.file)
            image_file = b64_bytes.decode("utf-8")
            images.append({"resultID" : image_data.resultID, "file" : image_file})
            print("added image.")
        else:
            print("Result ID: " + str(image_data.resultID) + " did not match requested: " + result_id)

    return jsonify({'images' : images})

@main.route('/api/sendfiles', methods=['POST'])
def sendfiles():
    # data comes in the format:
    # b'-----------------------------197130814939513389033381765664\r\nContent-Disposition: form-data; name="userID"; filename="XXXX.fa"\r\nContent-Type: application/octet-stream\r\n\r\nThese are the words I am writing.\r\n-----------------------------197130814939513389033381765664--\r\n'
    result_id = request.get_data()
    result_id = result_id.decode("utf-8")
    
    # remove the content not including the name sent by the front-end, which is the unique userID
    result_id = result_id.split(sep="name=\"")[1]
    result_id = result_id.split(sep="\"")[0]
    
    file_data = request.files[result_id]
    # TODO validate file
    #DEVELOPMENT
    file_path = 'api/api/tmp/' 
    #PRODUCTION
    #file_path = 'api/tmp/'
    file_data.save(os.path.abspath(file_path + file_data.filename))
    print("\n\n\n\n\n")

    # call Pascals script for fasta files here
    #DEVELOPMENT
    call = "api/api/propplotenv/bin/python api/api/propplot_v1_2.py " + "-id " + result_id + " -in " + file_path + file_data.filename + " -sf " + file_path + " -dbf api/dbs/"

    #PRODUCTION
    #call = "api/propplotenv/bin/python api/propplot_v1_2.py " + "-id " + result_id + " -in " + file_path + file_data.filename + " -sf " + file_path + " -dbf api/dbs/"
    subprocess.call(call, shell=True)

    # save the pdfs to the database
    prosite_file = open(os.path.abspath(file_path + result_id + "_ProteinGroup_prosite.pdf"), 'rb')
    prosite_db_entry = PDFModel(resultID=result_id, file=prosite_file.read())

    pfam_file = open(os.path.abspath(file_path + result_id + "_ProteinGroup_pfam.pdf"), 'rb')
    pfam_db_entry = PDFModel(resultID=result_id, file=pfam_file.read())

    combined_file = open(os.path.abspath(file_path + result_id + "_ProteinGroup_combined.pdf"), 'rb')
    combined_db_entry = PDFModel(resultID=result_id, file=combined_file.read())
    
    db.session.add(prosite_db_entry)
    db.session.add(pfam_db_entry)
    db.session.add(combined_db_entry)
    
    db.session.commit()

    # I have learned that we dont want to do this as the user may need to be able to access these files and may want to downlaod them
    # delete temp files
    # for f in glob.glob('api/tmp/'+result_id+'*'):
    #     print("Removing: " + str(f))
    #     os.remove(f)

    return "Done", 201

#after request [POST] requests only
#validate file exists, if it does, delete file
