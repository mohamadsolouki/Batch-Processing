import os
import tensorflow as tf
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Load the trained model
model = tf.keras.models.load_model('model/model.keras')

# Define the class labels (make sure these match your training data)
class_names = ['Apparel', 'Accessories', 'Footwear', 'Personal Care', 'Free Items', 'Sporting Goods']

# Define a function to preprocess the image
def preprocess_image(img):
    img = img.resize((160, 160))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Define a route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'files[]' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        files = request.files.getlist('files[]')
        predictions = []

        for file in files:
            # Save the file to the uploads folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Load and preprocess the image
            img = image.load_img(file_path, target_size=(160, 160))
            img = preprocess_image(img)

            # Make the prediction
            prediction = model.predict(img)
            class_index = np.argmax(prediction)
            class_label = class_names[class_index]
            probability = prediction[0][class_index]

            predictions.append({'filename': file.filename, 'class': class_label, 'probability': float(probability)})

        return jsonify(predictions)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')