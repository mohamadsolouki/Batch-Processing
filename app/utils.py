import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

model = load_model('../model/model.h5')

def preprocess_image(image):
    # Load the image
    img = load_img(image, target_size=(160, 160))
    
    # Convert the image to array
    img_array = img_to_array(img)
    
    # Normalize the image
    img_array = img_array / 255.0
    
    # Expand dimensions to match the model's input shape
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_batch(images):
    preprocessed_images = []
    for image in images:
        preprocessed_image = preprocess_image(image)
        preprocessed_images.append(preprocessed_image)
    
    preprocessed_images = np.vstack(preprocessed_images)
    predictions = model.predict(preprocessed_images)
    return predictions