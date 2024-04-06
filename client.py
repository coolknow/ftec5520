import requests

url = 'http://localhost:5000/addBlock'
data = {'username': 'user1', 'password': 'pass123'}

response1 = requests.post(url, json=data)
print(response1.text)

url = 'http://localhost:5000/check'
response2 = requests.get(url)
print(response2.text)