import requests

url = 'http://192.3.45.141:5000//predict'  # Replace with your server URL
files = [
    ('files[]', ('1163.jpg', open('data/images/1163.jpg', 'rb'), 'image/jpeg')),
    ('files[]', ('1164.jpg', open('data/images/1164.jpg', 'rb'), 'image/jpeg')),
    ('files[]', ('1165.jpg', open('data/images/1165.jpg', 'rb'), 'image/jpeg'))
]

response = requests.post(url, files=files)
predictions = response.json()

for prediction in predictions:
    print(f"Filename: {prediction['filename']}")
    for class_name, score in prediction['predictions']:
        print(f"{class_name}: {score:.2f}")
    print()