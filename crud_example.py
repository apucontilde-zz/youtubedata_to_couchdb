import requests
import datetime
import http.client
import json

SERVER_IP = "http://18.208.175.26"
SERVER_PORT = "5984"
headers = {"Host": "couchdb:5984", "Accept": "application/json"}
document = {
    "_id":"001",
    "nombre":"documento ejemplo",
    "valor numerico": 64546545
}

#CREATE
json_documment = json.dumps(document,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)
response = requests.put(
    SERVER_IP+":"+SERVER_PORT+"/crud_example/"+document['_id'], 
    json_documment.encode('utf-8')
)
print(response.json())


#READ
response = requests.get(
    SERVER_IP+":"+SERVER_PORT+"/crud_example/"+document['_id']
)
resp = response.json()
print(resp)
rev_id = resp['_rev']


#UPDATE
document_update = {
    "_rev":rev_id,
    "nombre":"documento ejemplo update",
    "valor numerico": 1
}
json_documment = json.dumps(document_update,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)
response = requests.put(
    SERVER_IP+":"+SERVER_PORT+"/crud_example/"+document['_id'], 
    json_documment.encode('utf-8')
)
print(response.json())
response = requests.get(
    SERVER_IP+":"+SERVER_PORT+"/crud_example/"+document['_id']
)
resp = response.json()
print(resp)
rev_id = resp['_rev']

#DELETE
response = requests.delete(
    SERVER_IP+":"+SERVER_PORT+"/crud_example/"+document['_id']+"?rev="+rev_id
)
resp = response.json()
print(resp)