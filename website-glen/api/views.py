from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/save_images', methods=['POST'])
def save_imgs():
    return 'Done', 201

@main.route('/images')
def images():
    images = []

    return jsonify({'images' : images})