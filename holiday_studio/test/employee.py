import json
import requests

base_url = "http://127.0.0.1:5000/employee"

# post employee
post_data = {"full_name": "Тестируемый",
             "email": "borsch@gmail.com",
             "login": "tasty",
             "password": "delicious",
             "phone": 23456}

post_employee_response = requests.post(base_url, json=post_data)
print("Post employee:", post_employee_response.json()
      , "http code:", post_employee_response.status_code)
employee_id = post_employee_response.json()["id"]

# get employees
get_employees_response = requests.get(base_url)
print("Get employees:", get_employees_response.json()
      , "http code:", get_employees_response.status_code)

# get employee
get_employee_response = requests.get(f"{base_url}/{employee_id}")
print(f"Get employee {employee_id}:", get_employee_response.json()
      , "http code:", get_employee_response.status_code)

# put employee
put_data = {"email": "testick@gmail.com",
            "full_name": "ТеСтОвЫй ХиП-хОп ЮзЕр",
            "phone": "lol"}
put_employee_response = requests.put(f"{base_url}/{employee_id}", json=put_data)
print(f"Put employee {employee_id}:", put_employee_response.json()
      , "http code:", put_employee_response.status_code)