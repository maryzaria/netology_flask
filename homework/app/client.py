import requests

# response = requests.post(
#     "http://127.0.0.1:5000/advertisements",
#     json={"title": "test2", "description": "Test advertisement", "owner": "Mary"},
# )

# response = requests.get(
#     'http://127.0.0.1:5000/advertisements',
# )

# response = requests.patch(
#     'http://127.0.0.1:5000/advertisements/1',
#     json={"description": "new_description"},
# )

# response = requests.delete(
#     'http://127.0.0.1:5000/advertisements/1',
# )

response = requests.post(
    'http://127.0.0.1:5000/login',
    json={"username": "maryz4456", "email": "zaripovam123@mail.ru", "password": "1234567893"}
)
# token = 'd1e23d73-9940-4209-9307-33de1ef821db'
# response = requests.patch(
#     'http://127.0.0.1:5000/user',
#     json={"username": "maryzaria", "email": "zaripovam123@mail.ru"},
#     headers={"Token": token},
# )
print(response.status_code)
print(response.json())
