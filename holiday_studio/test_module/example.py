import requests

data = {"full_name": "sosiska v teste",
        "phone": "88885555",
        "email": "toster@toster.ru",
        "login": "qwerty",
        "password": "12345"}
response = requests.post('http://127.0.0.1:5000/employee', json=data)
print(response.json())
