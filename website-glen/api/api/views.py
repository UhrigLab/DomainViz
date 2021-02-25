from flask import Blueprint, jsonify, request, redirect, current_app, render_template
from flask.helpers import send_file
from zipfile import ZipFile
import io
from os.path import basename

from werkzeug.exceptions import InternalServerError
#import py-fasta-validator # for validating fasta files
from api.utils import get_max_cookie, get_cookie_info, cleanup_cookies, save_fasta_file

import os, subprocess, base64, glob

#DEVELOPMENT
#api_path = "api/api/"
#PRODUCTION
api_path = "api/"

#DEVELOPMENT
#virtual_env = "api/api/propplotenvDEV/"
#PRODUCTION
virtual_env = "api/propplotenv/"

file_path = api_path + "tmp/"
example_file_path = api_path + "examples/"
example_fasta_file = "TAFIIsample_NAR_MS.fa"


main = Blueprint('main', __name__, static_folder="../build", static_url_path='/')

#TODO fix error handling
@main.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    # if original is None:
    #     # direct 500 error, such as abort(500)
    #     return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500.html", e=original), 500
@main.errorhandler(404)
def handle_404(e):
    return render_template("404.html", e=e), 404

@main.route('/')
def index():
    return main.send_static_file('index.html')

@main.route('/api/testFasta')
def test_fasta():
    return send_file(os.path.abspath(example_file_path + example_fasta_file), as_attachment=True)
# @main.route('/api/testResults')
# def test_results():
#     result_id = "example"
#     result_zip = ZipFile(example_file_path + result_id + '.zip', 'w')

#     for f in glob.glob(example_file_path+result_id+'*.pdf'):
#         result_zip.write(f, basename(f))
#         print("added pdf: " + f)
#     for f in glob.glob(example_file_path+result_id+'*.tsv'):
#         result_zip.write(f, basename(f))
#         print('added tsv: ' + f)
#     for f in glob.glob(example_file_path+result_id+'*.txt'):
#         result_zip.write(f, basename(f))
#     for f in glob.glob(example_file_path+'README.md'):
#         result_zip.write(f, basename(f))
#     result_zip.close()

#     return send_file(os.path.abspath(example_file_path + result_id + '.zip'), as_attachment=True)



@main.route('/api/images/<username>')
def images(username):
    result_id = username
    pdf_names = []
    # sort the list of pdfs associated with the result_id
    for f in glob.glob(os.path.abspath(file_path+result_id+'*.pdf')):
        #get the result_id from the filename to ensure we have to correct files
        file_id = f.split("tmp/")[1]
        file_id = file_id.split("_")[0]
        if result_id == file_id:
            pdf_names.append(f)
    pdf_names=sorted(pdf_names)
    
    # open the files in order of their name (for consistency of display) and add them to the list of pdfs
    pdfs = []
    for f in pdf_names:
        file = open(f, 'rb')
        b64_bytes = base64.b64encode(file.read())
        image_file = b64_bytes.decode("utf-8")
        pdfs.append({"resultID" : result_id, "file" : image_file})
        print("added image: " + f)
        file.close()
    max_cookie = get_max_cookie(file_path, result_id)
    #TODO swap temp with correct
    #temp
    if len(pdfs) < 3 and max_cookie:
        if get_cookie_info(file_path, result_id, max_cookie):
            return jsonify({'failed' : max_cookie, 'info' : " ".join(get_cookie_info(file_path, result_id, max_cookie).split())})
        else:
            return jsonify({'failed' : max_cookie})
    elif len(pdfs) < 3:
        return jsonify({'failed' : 'null'})
    else:
        cleanup_cookies(file_path, result_id)
        return jsonify({'images' : pdfs})
    #correct
    # if len(pdfs) == 0 and max_cookie:
    #     if get_cookie_info(result_id, max_cookie):
    #         return jsonify({'failed' : max_cookie, 'info' : " ".join(get_cookie_info(result_id, max_cookie).split())})
    #     else:
    #         return jsonify({'failed' : max_cookie})
    # elif len(pdfs) == 0:
    #     return jsonify({'failed' : 'null'})
    # else:
    #     cleanup_cookies(result_id)
    #     return jsonify({'images' : pdfs})

@main.route('/api/sendfiles', methods=['POST'])
def sendfiles():
    # retrieve the fasta file(s) from the POST
    print(request.files)
    # Each file in request.files has the layout:
    # (file_name<str>, file<FileStorage>, result_id<str>)
    result_id = ""
    fasta_file = None
    fasta_filename = None
    fp = file_path

    i=0 
    for key in request.files.keys():
        fasta_file=request.files[key]
        group_name=key
        print(fasta_file)
         # A failsafe in case the wrong type of files have been uploaded. In this case, we ignore it, and move on to the next file
        if ".fa" not in group_name and ".fasta" not in group_name:
            print("File " + group_name + " is not a fastafile, and is being skipped.")
            continue
        if i==0:
            #retrieve result id
            result_id=fasta_file.filename # this is called filename because normally the request.files has a different layout than the one i am using
        
        # Save each fasta file in an increasingly large single fasta file called result_id.fa
        # Each header will have its group name 
        # Eg. e23f6b67.163d.2103.1984.b6937bf3518a.fa
        fasta_filename = result_id + ".fa"
        group_name = group_name.split(".")[0] # remove the .fa from group_name
        save_fasta_file(fp, fasta_file, result_id, group_name)

        print("Fasta file: " + group_name + " has been saved as " + fasta_filename)
        i+=1

    if fasta_file == None:
        for key in request.form.keys():
            if i==0:
                result_id=key
                break
        fasta_filename=example_fasta_file
        fp = example_file_path
        print("Test fasta file being used")

    # retrieve the 4 parameters
    absolute_results=request.form["absoluteResults"]
    ar = "0"
    if absolute_results == "true": # will be true or false, but the script needs 0 or 1
        ar = "1"
    cutoff = request.form["cutoff"]
    max_cutoff = request.form["maxCutoff"]
    scale_figure = request.form["scaleFigure"]
    custom_scaling = "1"
    if scale_figure == "1":
        custom_scaling = "0" 

    # Set up the call for Pascals script here
    call = virtual_env +  "bin/python " + api_path + "propplot_v1_2.py " + "-id " + result_id + " -in " + fp + fasta_filename + " -sf " + file_path + " -dbf " + api_path + "dbs/" + " -ar " + ar + " -cut " + cutoff + " -mcut " + max_cutoff + " -cs " + custom_scaling + " -api " + scale_figure
    
    #add the protein groups file, the creation of which can be found in utils.py
    if fasta_filename != example_fasta_file:
        protein_groups_filename = result_id + "_groupfile.tsv"
        call = call + ' -gf ' + file_path + protein_groups_filename

    print(call)

    # try to retrieve the other 2 files, if they exist
    # color_file = None
    # ignore_domains_file = None
    # try:
    #     color_file = request.files["colorFile"]
    #     color_file.save(os.path.abspath(file_path + color_file.filename))
    #     call = call + ' -cf ' + file_path + color_file.filename
    # except:
    #     print("no color file")
    # try:
    #     ignore_domains_file = request.files["ignoreDomains"]
    #     ignore_domains_file.save(os.path.abspath(file_path + ignore_domains_file.filename))
    #     call = call + ' -if ' + ignore_domains_file.filename
    # except:
    #     print("no ignore domains file")

    #send the call
    subprocess.Popen(call, shell=True)

    return "Done", 201


@main.route('/api/download/<username>', methods=['GET', 'POST'])
def download(username):
    result_id = username
    result_zip = ZipFile(file_path + result_id + '.zip', 'w')

    for f in glob.glob(file_path+result_id+'*.pdf'):
        result_zip.write(f, basename(f))
        print("added pdf: " + f)
    for f in glob.glob(file_path+result_id+'*.tsv'):
        result_zip.write(f, basename(f))
        print('added tsv: ' + f)
    for f in glob.glob(file_path+result_id+'*.txt'):
        result_zip.write(f, basename(f))
    for f in glob.glob(example_file_path+'README.md'):
        result_zip.write(f, basename(f))
    result_zip.close()
    
    return send_file(os.path.abspath(file_path + result_id + '.zip'), as_attachment=True)

#after request [POST] requests only
#validate file exists, if it does, delete file
