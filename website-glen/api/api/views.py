from flask import Blueprint, jsonify, request, redirect, current_app
from flask.helpers import send_file, send_from_directory, url_for
from zipfile import ZipFile
import io
from api.__init__ import db
from api.models import PDFModel
from api.utils import get_max_cookie

import os, subprocess, base64, glob

main = Blueprint('main', __name__, static_folder="../build", static_url_path='/')
@main.route('/')
def index():
    return main.send_static_file('index.html')

@main.route('/api/images/<username>')
def images(username):
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
    
    if len(images) == 0 and get_max_cookie(result_id):
        return jsonify({'failed' : get_max_cookie(result_id)})
    elif len(images) == 0:
        return jsonify({'failed' : 'null'})
    else:
        return jsonify({'images' : images})

@main.route('/api/sendfiles', methods=['POST'])
def sendfiles():
    # retrieve the data from the POST
    result_id = ""
    fasta_file = None
    i=0 # the first key will always be the result id, and its value will always be the fasta file
    for key in request.files.keys():
        if i==0:
            #retrieve fasta file
            result_id=key
            fasta_file=request.files[key]
            break
    if fasta_file == None:
        return "No fasta file", 500
    
    # try to retrieve the other 3 files, if they exist
    protein_groups_file = None
    color_file = None
    ignore_domains_file = None
    try:
        protein_groups_file = request.files["proteinGroups"]
    except:
        print("no protein groups file")
    try:
        color_file = request.files["colorFile"]
    except:
        print("no color file")
    try:
        ignore_domains_file = request.files["ignoreDomains"]
    except:
        print("no ignore domains file")
    # TODO validate files


    absolute_results=request.form["absoluteResults"]
    cutoff = request.form["cutoff"]
    max_cutoff = request.form["maxCutoff"]
    scale_figure = request.form["scaleFigure"]

    
    #DEVELOPMENT
    file_path = 'api/api/tmp/' 
    #PRODUCTION
    #file_path = 'api/tmp/'


    fasta_file.save(os.path.abspath(file_path + fasta_file.filename))

    # call Pascals script for fasta files here
    #DEVELOPMENT
    call = "api/api/propplotenvDEV/bin/python api/api/propplot_v1_2.py " + "-id " + result_id + " -in " + file_path + fasta_file.filename + " -sf " + file_path + " -dbf api/dbs/"

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

    return "Done", 201


@main.route('/api/download/<username>', methods=['GET', 'POST'])
def download(username):
    result_id = username
    #DEVELOPMENT
    file_path = 'api/api/tmp/' 
    #PRODUCTION
    #file_path = 'api/tmp/'
    print("zipfile")
    # bytes_file = BytesIO()
    result_zip = ZipFile(file_path + result_id + '.zip', 'w')

    for f in glob.glob(file_path+result_id+'*.pdf'):
        result_zip.write(f)
        print("added pdf: " + f)
    for f in glob.glob(file_path+result_id+'*.csv'):
        result_zip.write(f)
        print('added csv: ' + f)
    for f in glob.glob(file_path+result_id+'*.tsv'):
        result_zip.write(f)
        print('added csv: ' + f)
    result_zip.close()
    print("closed")
    
    return send_file(os.path.abspath(file_path + result_id + '.zip'), as_attachment=True)

#after request [POST] requests only
#validate file exists, if it does, delete file
