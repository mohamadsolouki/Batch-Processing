from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
import io

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('fashion_model.h5')

def prepare_image(img):
    """
    Convert image to the format the model expects.
    """
    img = Image.open(io.BytesIO(img))
    img = img.resize((160, 160))
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/predict', methods=['POST'])
def predict():
    data = request.files['image'].read()
    image = prepare_image(data)
    predictions = model.predict(image)
    return jsonify(predictions.tolist())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)