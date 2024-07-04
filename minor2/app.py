
from flask import Flask, render_template, request
from steg_functions import encode_img_data, decode_img_data
import cv2
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode_image', methods=['GET', 'POST'])
def encode_image():
    if request.method == 'POST':
        image_file = request.files['image']
        data = request.form['data']
        if image_file:
            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            name = 'encoded_image.png'
            encode_img_data(img, data, name)
            return render_template('success.html', message="Image successfully encoded!")
    return render_template('encode_image.html')

@app.route('/decode_image', methods=['GET', 'POST'])
def decode_image():
    if request.method == 'POST':
        stego_image = request.files['stego_image']
        if stego_image:
            img = cv2.imdecode(np.frombuffer(stego_image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            decoded_data = decode_img_data(img)
            return render_template('success.html', message="Data extracted successfully!", data=decoded_data)
    return render_template('decode_image.html')

if __name__ == '__main__':
    app.run(debug=True)