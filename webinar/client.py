import requests

response = requests.post(
    "http://127.0.0.1:5000/user",
    json={"name": "user_4", "password": "123раслпмплпм"},
    # headers={"token": "secret"},
)

# response = requests.get(
#     'http://127.0.0.1:5000/user/12',
# )

# response = requests.patch(
#     'http://127.0.0.1:5000/user/12',
#     json={"name": "user_3"},
# )

# response = requests.delete(
#     'http://127.0.0.1:5000/user/12',
#
# )
print(response.status_code)
print(response.json())
