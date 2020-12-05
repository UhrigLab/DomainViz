from flask import Blueprint, jsonify, request, redirect, current_app
from flask.helpers import send_file
from zipfile import ZipFile
import io
#import py-fasta-validator # for validating fasta files
from api.utils import get_max_cookie

import os, subprocess, base64, glob

#DEVELOPMENT
#file_path = 'api/api/tmp/' 
#PRODUCTION
file_path = 'api/tmp/'

main = Blueprint('main', __name__, static_folder="../build", static_url_path='/')
@main.route('/')
def index():
    return main.send_static_file('index.html')

@main.route('/api/images/<username>')
def images(username):
    result_id = username
    images = []
    for f in glob.glob(file_path+result_id+'*.pdf'):
        file = open(f, 'rb')
        b64_bytes = base64.b64encode(file.read())
        image_file = b64_bytes.decode("utf-8")
        images.append({"resultID" : result_id, "file" : image_file})
        print("added image: " + f)
    
    if len(images) == 0 and get_max_cookie(result_id):
        return jsonify({'failed' : get_max_cookie(result_id)})
    elif len(images) == 0:
        return jsonify({'failed' : 'null'})
    else:
        return jsonify({'images' : images})

@main.route('/api/sendfiles', methods=['POST'])
def sendfiles():

    # retrieve the fasta file from the POST
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
    fasta_file.save(os.path.abspath(file_path + fasta_file.filename))

    # retrieve the 4 parameters
    absolute_results=request.form["absoluteResults"]
    ar = "0"
    if absolute_results == "true": # will be true or false, but the script needs 0 or 1
        ar = "1"
    cutoff = request.form["cutoff"]
    max_cutoff = request.form["maxCutoff"]
    scale_figure = request.form["scaleFigure"]

     # call Pascals script for fasta files here
    #DEVELOPMENT
    #call = "api/api/propplotenvDEV/bin/python api/api/propplot_v1_2.py " + "-id " + result_id + " -in " + file_path + fasta_file.filename + " -sf " + file_path + " -dbf api/api/dbs/" + " -ar " + ar + " -cut " + cutoff + " -mcut " + max_cutoff + " -sbp " + scale_figure
    #PRODUCTION
    call = "api/propplotenv/bin/python api/propplot_v1_2.py " + "-id " + result_id + " -in " + file_path + fasta_file.filename + " -sf " + file_path + " -dbf api/dbs/" + " -ar " + ar + " -cut " + cutoff + " -mcut " + max_cutoff + " -sbp " + scale_figure
    
    # try to retrieve the other 3 files, if they exist
    protein_groups_file = None
    color_file = None
    ignore_domains_file = None
    try:
        protein_groups_file = request.files["proteinGroups"]
        protein_groups_file.save(os.path.abspath(file_path + protein_groups_file.filename))
        call = call + ' -gf ' + file_path + protein_groups_file.filename
    except:
        print("no protein groups file")
    try:
        color_file = request.files["colorFile"]
        color_file.save(os.path.abspath(file_path + color_file.filename))
        call = call + ' -cf ' + file_path + color_file.filename
    except:
        print("no color file")
    try:
        ignore_domains_file = request.files["ignoreDomains"]
        ignore_domains_file.save(os.path.abspath(file_path + ignore_domains_file.filename))
        call = call + ' -if ' + ignore_domains_file.filename
    except:
        print("no ignore domains file")
    # TODO validate files

    subprocess.Popen(call, shell=True)

    return "Done", 201


@main.route('/api/download/<username>', methods=['GET', 'POST'])
def download(username):
    result_id = username
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
    
    return send_file(os.path.abspath(file_path + result_id + '.zip'), as_attachment=True)

#after request [POST] requests only
#validate file exists, if it does, delete file
