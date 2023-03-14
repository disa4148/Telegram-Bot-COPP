import requests
import json
import main


#JSON для мероприятий
#response = requests.get('https://www.mininghamster.com/api/v2/aI6dgBApSPbph0kDISXNCaoHYvVgXTfS')
#print(response.json()[0]['success'])


# f = json.loads("CategoriesInfo.json")
#
# for item in f:
#     print(item)

#with open('CategoriesInfo.json', encoding='utf-8') as f:
 #   data = f.read()
 #   categories = json.loads(data)

#for i in categories:
#    print(i)
#    for j in categories[i]:
#        print(j)

users = {}
users.update({message.chat.id : value})
for i in main.users:
    print(i)