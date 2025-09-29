import requests

url = 'http://127.0.0.1:8000/api/users/login/'
data = {'facebook_id': '123456'}

response = requests.post(url, json=data)
print(response.status_code)
print(response
