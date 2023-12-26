import requests

# response = requests.post(
#     "http://127.0.0.1:5000/advertisements",
#     json={"title": "test",
#           "description": "Test advertisement",
#           "owner": "Mary11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
#           }
# )

# response = requests.get(
#     'http://127.0.0.1:5000/advertisements/1',
# )

# response = requests.patch(
#     'http://127.0.0.1:5000/advertisements/1',
#     json={"description": "new_description"},
# )

response = requests.delete(
    'http://127.0.0.1:5000/advertisements/1',
)
print(response.status_code)
print(response.json())
