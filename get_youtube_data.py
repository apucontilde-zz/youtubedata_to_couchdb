#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import codecs
import argparse
import collections
import http.client
import json
import uuid
from time import time, sleep
from datetime import timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SERVER_IP = "34.239.140.119"
SERVER_PORT = 5984
max_results=40
headers = {"Host": "couchdb:5984", "Accept": "application/json"}


def youtube_search(keywords, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    
    tag_ref_documents = []
    tag_nest_documents = []
    video_documents = []
    tags = dict()
    for keyword in keywords.split(';'):
        sleep(1)
        try:
            print (keyword)
            search_response = youtube.search().list(
                part='id,snippet',
                maxResults=max_results,
                q=keyword,
                type='video'
            ).execute()
            
            

            # Add each result to the appropriate list, and then display the lists of
            # matching videos, channels, and playlists.
            videos = []
            for search_result in search_response.get('items', []):
                    videos.append('%s' % (search_result['id']['videoId']))
            
            videos_id_query = ','.join(videos)
            search_response = youtube.videos().list(
                id=videos_id_query,
                part='snippet,statistics',
                maxResults=max_results,
            ).execute()

            


            for search_result in search_response.get('items', []):
                if ( 'tags' in search_result['snippet']):
                    video_dict = {
                    "doc_type":"video",
                    "videoId" : search_result['id'],
                    "title": search_result['snippet']['title'], 
                    "description": search_result['snippet']['description'], 
                    "publishedAt": search_result['snippet']['publishedAt'], 
                    "statistics" : search_result['statistics']} 
                    for tag in search_result['snippet']['tags']:
                            if tag not in tags:
                                tags[tag] = []
                            tags[tag].append(video_dict)
        except Exception as e:
            print(str(e)) 


    #tags = sorted(tags.items(), key=lambda x: len(x[1]),reversed=True)
    videos = dict()
    for tag, tag_videos in tags.items():
        if len(tag_videos) > 6 :
            try:
                #with referenced videos
                tagId = tag.replace(' ','_')
                tag_ref_dict = {
                    "doc_type": "tag_reference",
                    "tagId": tagId,
                    "tag": tag ,
                    "videos":[vid['videoId'] for vid in tag_videos]}
                tag_document = json.dumps(tag_ref_dict,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)
                tag_ref_documents.append(tag_document)
                tag_document = tag_document.encode('utf-8')
                conn = http.client.HTTPConnection(SERVER_IP,SERVER_PORT)
                conn.request("PUT", "/youtube_data/"+tagId, tag_document,headers)
                response = conn.getresponse()
                print("TAG_REF:",response.status, response.reason)

                for video_dict in tag_videos:
                    if video_dict['videoId'] not in videos:
                        videos[video_dict['videoId']] = video_dict
            
                #with nested videos
                tagId = tag.replace(' ','_')+"_nested"
                tag_nest_dict = {
                    "doc_type": "tag_nested",
                    "tagId": tagId,
                    "tag": tag ,
                    "videos":tag_videos}
                tag_document = json.dumps(tag_nest_dict,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)
                tag_nest_documents.append(tag_document)
                tag_document = tag_document.encode('utf-8')
                conn = http.client.HTTPConnection(SERVER_IP,SERVER_PORT)
                conn.request("PUT", "/youtube_data/"+tagId, tag_document,headers)
                response = conn.getresponse()
                print("TAG_NEST:",response.status, response.reason)
            except Exception as e:
                print(str(e)) 
        
    for video_key, video_dict in videos.items():
        try:
            video_documment = json.dumps(video_dict,sort_keys=True,indent=4, separators=(',', ': '),ensure_ascii=False)
            video_documents.append(video_documment)
            #print(video_documment)
            conn = http.client.HTTPConnection(SERVER_IP,SERVER_PORT)
            conn.request("PUT", "/youtube_data/"+str(video_dict['videoId']), video_documment.encode('utf-8'),headers)
            response = conn.getresponse()
            #print(video_documment)
            print(response.status, response.reason)
        except Exception as e:
            print(str(e)) 
    
    
    # #[print(repr(tag)+"\n") for tag in most_videos]
    # import datetime
    # datestr = datetime.datetime.now().strftime('%b-%d-%I%M%p-%G')
    # with open('videos'+datestr+'_'+keywords,'w') as videofile:
    #     with open('tags_ref'+datestr+'_'+keywords,'w') as tagreffile :
    #         with open('tags_nest'+datestr+'_'+keywords,'w') as tagnestfile :
    #             videofile.write(str(video_documents), encode='utf8')
    #             tagreffile.write(str(tag_ref_documents).encode('utf8'))
    #             tagnestfile.write(str(tag_nest_documents).encode('utf8'))
  


if __name__ == '__main__':
    keywords='prose;frog;silk;pollution;hole;hair;fall;zinc;letters;grip;governor;rule;yard;quilt;dock;waste;turn;friend;trouble;downtown;hand;apparatus;store;oil;stem;honey;regret;development;chalk;noise;brick;gate;achiever;cherry;plot;knowledge;bike;wall;building;fish;play;burst;toys;birth;advice;spring;shelf;number;shake;steam;chin;wish;chess;dogs;flavor;mice;current;event;wax;drink;books;degree;town;water;voyage;bulb;use;curtain;dinosaurs;kittens;sock;request;lace;bee;treatment;pump;breath;way;home;walk;story;teeth;tendency;fire;swing;skirt;bikes;calculator;appliance;industry;thrill;quiver;roof;soap;cloth;hands;activity;fear;crate;increase'
    youtube_search(keywords,max_results)