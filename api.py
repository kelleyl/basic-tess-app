#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pytesseract
import numpy
import cv2

application = Flask(__name__)
api = Api(application)

# @application.route('/')
# def index():
#     return "Index Page"

def get_text(image):
    proc = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # proc = cv2.threshold(proc, 0, 255,
    #                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    proc = cv2.medianBlur(proc, 3)
    text = pytesseract.image_to_string(image)
    return text

class TestAPI(Resource):
    def get(self):
        print("GET request called")
        return 'Barebone flask rest api served using docker...'

    def post(self):
        #from https://stackoverflow.com/questions/47515243/reading-image-file-file-storage-object-using-cv2
        # read image file string data
        print (request.files)
        filestr = request.files['image'].read()
        # convert string data to numpy array
        npimg = numpy.fromstring(filestr, numpy.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        return get_text(img)

api.add_resource(TestAPI, '/')

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)

