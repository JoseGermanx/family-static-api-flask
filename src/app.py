"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member', methods=['POST'])
def add_member():
    try:
        request_body = request.get_json()
        if request_body is None:
            return "The request body is null", 400
        if "first_name" not in request_body:
            return "The request body is missing the first_name property", 400
        if "age" not in request_body:
            return "The request body is missing the age property", 400
        if "lucky_numbers" not in request_body:
            return "The request body is missing the lucky_numbers property", 400
        
        jackson_family.add_member(request_body)
        return jsonify(request_body), 200
    except Exception as e:
        return str(e), 500

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if member is None:
            return "Member not found", 404
        return jsonify(member), 200
    except Exception as e:
        return str(e), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if id not in request.args:
           return "Id member its missing", 400
    jackson_family.delete_member(id)
    return jsonify({"done": True}), 200

@app.route('/members', methods=['GET'])
def get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
