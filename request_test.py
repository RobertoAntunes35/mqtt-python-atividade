import requests

i = 10


url = "http://localhost:5000/api-roberto/v1/create-new-data/temp"
while True:
    local = "Area - Impar"
    i = i + 1

    if i % 2 == 0:
        local = "Area - Par"
    data = {
        "local":local,
        "value":i,
        "type":"temp"
    }

    requests.post(url, data=data)
    
    





