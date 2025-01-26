import json
import os
import time

logCredsPath = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\logCreds\testToken.json'

user = {
            "method" : "login",
            "username" : "username",
            "password" : "password"
        }

parsed = json.dumps(user)
print(user['method'])
with open(logCredsPath, 'w') as file:
    try:
        file.write(parsed)
    except Exception as e:
        print(e)

time.sleep(5)
os.remove(logCredsPath)