import requests
import json


#JSON для мероприятий
#response = requests.get('https://dev.copp42.ru/programs')
#print(response.json()[0]['name'])

string = '{"answer": "Hello, bro, I am working!"}'
o = json.loads(string)
print(o['answer'])