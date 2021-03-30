from flask import Blueprint, jsonify, request, redirect, current_app, render_template
from flask.helpers import send_file
from zipfile import ZipFile
import io
from os.path import basename

from werkzeug.exceptions import InternalServerError
#import py-fasta-validator # for validating fasta files
from api.utils import get_max_cookie, get_cookie_info, cleanup_cookies, save_fasta_file, get_pdf_names, get_group_names

import os, subprocess, base64, glob

#DEVELOPMENT
api_path = "api/api/"
#PRODUCTION
#api_path = "api/"

#DEVELOPMENT
virtual_env = "api/api/propplotenvDEV/"
#PRODUCTION
#virtual_env = "api/propplotenv/"

file_path = api_path + "tmp/"
example_file_path = api_path + "examples/"
example_multiple_files = {"single_test": "GNATs_ALL.fa", "mult_test_1": "GNATs_class1.fa", "mult_test_2": "GNATs_class2.fa", "mult_test_3": "GNATs_class3.fa"}


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

#Send the hand-made 'example.zip' file to the user
@main.route('/api/testFasta')
def test_fasta():
    return send_file(os.path.abspath(example_file_path + "example.zip"), as_attachment=True)

@main.route('/api/color-files/<username>', methods=['GET'])
def colorFiles(username):
    result_id = username
    color_file = open(os.path.abspath(file_path+result_id+"_domain_color_file.txt"), 'r')
    lines = color_file.readlines()

    return jsonify({'colorGroups' : lines})

@main.route('/api/images/<username>')
def images(username):
    result_id = username

    # get and sort the list of pdfs, and the list of groups associated with the result_id
    pdf_names = get_pdf_names(file_path, result_id)
    pdf_names = sorted(pdf_names)

    # if there are no pdfs, then there cant be any groups (or rather, even if there are groups, we have to return a failed status
    # since domainviz.py isnt finished yet)
    if len(pdf_names) > 0:
        group_names = get_group_names(file_path, result_id)
        group_names = sorted(group_names)
    else:
        group_names = []
    


    
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
    
    # First we check if there are any groups, if there aren't, then something went wrong, and we return 'failed'
    if len(group_names) < 1 and max_cookie:
        if get_cookie_info(file_path, result_id, max_cookie):
            return jsonify({'failed': max_cookie, 'info': " ".join(get_cookie_info(file_path, result_id, max_cookie).split())})
        else:
            return jsonify({'failed': max_cookie})
    elif len(group_names) < 1: 
        return jsonify({'failed': 'null'})
    # If there are groups, we need to wait until there are 3 pdfs per group in order to display them. 
    # Otherwise, we will display a bunch of broken or half-made data.
    if len(pdfs) < (3*len(group_names)) and max_cookie:
        if get_cookie_info(file_path, result_id, max_cookie):
            return jsonify({'failed': max_cookie, 'info': " ".join(get_cookie_info(file_path, result_id, max_cookie).split())})
        else:
            return jsonify({'failed': max_cookie})
    elif len(pdfs) < (3*len(group_names)):
        return jsonify({'failed': 'notready'})
    else:
        cleanup_cookies(file_path, result_id)
        return jsonify({'images': pdfs, 'groups': group_names})

@main.route('/api/sendfiles', methods=['POST'])
def sendfiles():
    # retrieve the fasta file(s) from the POST
    # Each file in request.files has the layout:
    # (file_name<str>, file<FileStorage>, result_id<str>)
    result_id = ""
    fasta_file = None
    fasta_filename = None

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
        group_name = group_name.split(".")[0] # remove the .fa from group_name
        save_fasta_file(file_path, fasta_file, result_id, group_name)
        i+=1

    # This block runs if there are no files being sent to the backend, in which case, there is a form sent instead
    # that just has the name of the group that the test file should be saved under.
    if fasta_file == None:
        # Start i at -1 because the first key-value pair will always be "result_id": the_result_id_for_this_job
        i=-1
        result_id=request.form['result_id']
        print(request.form)
        for key in request.form.keys():
            # if the form contains a .fa or .fasta file, we save it as such, if not, ignore it
            if '.fa' in request.form[key]:
                # set the variables for the call to the example variables, and "save" the fasta file.
                group_name = request.form[key].split('.fa')[0]  # remove the .fa from group_name    
                #key will be "testX" where X is the number. This key is passed to the example_multiple_files dictionary, which is then
                #used to grab the correct test file.
                save_fasta_file(example_file_path, example_multiple_files[key], result_id, group_name) 
            i=i+1
        print("Test fasta file(s) being used")

    # fasta_filename will always be:
    fasta_filename = result_id + ".fa"

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
    call = virtual_env +  "bin/python " + api_path + "domainviz.py " + "-id " + result_id + " -in " + file_path + fasta_filename + " -sf " + file_path + " -dbf " + api_path + "dbs/" + " -ar " + ar + " -cut " + cutoff + " -mcut " + max_cutoff + " -cs " + custom_scaling + " -api " + scale_figure
    
    #add the protein groups file, the creation of which can be found in utils.py
    protein_groups_filename = result_id + "_groupfile.tsv"
    call = call + ' -gf ' + file_path + protein_groups_filename

    # try to retrieve the other 2 files, if they exist
    # This functionality is currently disabled.
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


@main.route('/api/u-motif', methods=["POST"])
def u_motif():
    # retrieve the fasta file(s) from the POST
    # Each file in request.files has the layout:
    # (<foreground or background><str>, file<FileStorage>, file_name<str>)
    # Eg. ("foreground", <FileStorage: file_name ('application/octet-stream')>)
    result_id=request.form['result_id']
    # initalize these as None so that later on we can tell if they were saved as files, or if they need to be saved
    # as text, or if example files need to be used.
    fg_fasta_file = None
    bg_fasta_file = None

    # assign all files to their respective locations
    for key in request.files.keys():
        file=request.files[key]
        file_name=key
        fg_bg=file.filename # a technical misuse of this variable, but it works for our purposes
        
         # A failsafe in case the wrong type of files have been uploaded. In this case, we ignore it, and move on to the next file
        if ".fa" not in file_name and ".fasta" not in file_name:
            print("File " + file_name + " is not a fastafile, and is being skipped.")
            continue

        if fg_bg == "foreground":            
            fg_fasta_file=result_id + "_fg.fa"
            file.save(file_path + fg_fasta_file)
        else:
            bg_fasta_file=result_id + "_bg.fa"
            file.save(file_path + bg_fasta_file)

    # This block runs if there are no files being sent to the backend, in which case, there is a form sent instead
    # that just has the name of the group that the test file should be saved under.
    if fg_fasta_file == None:
        for key in request.form.keys():
            # if the form contains a .fa or .fasta file, we save it as such, if not, ignore it  
            if key == "manual":
                fg_filename=request.form[key]
                fg_text=request.form[fg_filename]
                f = open(fg_filename)
                print("manual file found")
                #TODO save fasta text
            elif key == "test": # currently only have a single test file
                fg_fasta_filename=example_multiple_files["single_test"]
                print("test file found")
    
    if bg_fasta_file == None:

        for key in request.form.keys():
            # if the form contains a .fa or .fasta file, we save it as such, if not, ignore it
            if '.fa' in request.form[key]:
                # set the variables for the call to the example variables, and "save" the fasta file.
                group_name = request.form[key].split('.fa')[0]  # remove the .fa from group_name    
                #key will be "testX" where X is the number. This key is passed to the example_multiple_files dictionary, which is then
                #used to grab the correct test file.
   #             save_fasta_file(example_file_path, example_multiple_files[key], result_id, group_name) 


    # we want the outputs saved to result_id.whatever for easy retrieval later
    save_to = result_id

    return "Done", 201
#after request [POST] requests only
#validate file exists, if it does, delete file
