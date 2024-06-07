import requests
import os

url = 'http://192.3.45.141:5000//predict'  # Replace with your server URL
test_images_dir = 'test-images'
files = []

# Loop through all files in the test-images directory
for filename in os.listdir(test_images_dir):
    # Only add files with .jpg extension
    if filename.endswith('.jpg'):
        file_path = os.path.join(test_images_dir, filename)
        files.append(('files[]', (filename, open(file_path, 'rb'), 'image/jpeg')))

response = requests.post(url, files=files)
predictions = response.json()

for prediction in predictions:
    print(f"Filename: {prediction['filename']}")
    for class_name, score in prediction['predictions']:
        print(f"{class_name}: {score:.2f}")
    print()