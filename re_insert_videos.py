import requests
import json
import http.client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import traceback
SERVER_IP = "ec2-3-84-228-227.compute-1.amazonaws.com"
SERVER_PORT = 5984
headers = {"Host": "couchdb:5984", "Content-Type": "application/json"}
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
max_results=40

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

videos = dict()
response = requests.get(url = "http://ec2-3-84-228-227.compute-1.amazonaws.com:5984/youtube_data/_design/doc_type/_view/tag_nested")
for doc in response.json()['rows']:
    for video in doc['value']:
        if video['videoId'] not in videos:
            videos[video['videoId']] = video


response = requests.get(url = "http://ec2-3-84-228-227.compute-1.amazonaws.com:5984/youtube_data/_design/doc_type/_view/tag_reference?include_docs=true")

for doc in response.json()['rows']:
    if(doc['doc'] is None):
        try:
            videoId = doc['value']['_id']
            if videoId not in videos:
                print("no vid found with id ",videoId," in tag ", doc['id'])
            else:
                video_dict = videos[videoId]
                if videoId[0]=="_":
                    videoId="-"+videoId
                video_documment = json.dumps(video_dict,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)


                conn = http.client.HTTPConnection(SERVER_IP,SERVER_PORT)
                conn.request("PUT", "/youtube_data/"+videoId, video_documment.encode('utf-8'),headers)
                insert_response = conn.getresponse()

                print(insert_response.status, insert_response.reason)
                if insert_response.status != 201:
                    print (insert_response)
                    print (video_documment)
        except Exception:
            print(traceback.format_exc()) 


#         try:
#             video_documment = json.dumps(video,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)
#             conn = http.client.HTTPConnection(SERVER_IP,SERVER_PORT)
#             conn.request("PUT", "/youtube_data/"+str(video['videoId']), video_documment.encode('utf-8'),headers)
#             response = conn.getresponse()
#             print(response.status, response.reason)
#         except Exception as e:
#             print(str(e))   