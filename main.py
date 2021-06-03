# main script fetch top tracks
import os
import json
import requests
import csv
import boto3
from botocore.exceptions import ClientError
import datetime

token = os.environ['SPOTIFY_TOKEN']
token_endpoint = 'https://accounts.spotify.com/api/token'
payload = {'grant_type': 'client_credentials'}
headers = {'Authorization': 'Basic {}'.format(token)}

bz = '7i9bNUSGORP5MIgrii3cJc'
param_market = 'JP'
top_tracks_endpoint = 'https://api.spotify.com/v1/artists/{}/top-tracks?market={}'.format(bz, param_market)

top_ten_track_list = []
s3_client = boto3.client('s3')

now = datetime.datetime.now()
filename = 'bz/result_{0:%Y%m%d}.csv'.format(now)

def fetch_top_tracks():
    # get bearer token
    token_res = requests.post(token_endpoint, headers=headers, data=payload)
    access_data = token_res.json()
    access_token = access_data['access_token']

    header_params = {'Authorization': 'Bearer {}'.format(access_token)}

    res = requests.get(top_tracks_endpoint, headers=header_params)
    res_data = res.json()
    track_list = res_data['tracks']

    keys =set(["name", "popularity", "uri"])
    for track in track_list:
        result = dict(filter(lambda x: x[0] in keys, track.items()))
        top_ten_track_list.append(result)

    track_rank = sorted(top_ten_track_list, key=lambda x: x['popularity'], reverse=True)
    print(track_rank)
    write_csv(track_rank)
    upload_file(filename, 'spotify-top10-tracks')

csv_columns = ['name', 'popularity', 'uri']

def write_csv(list):
    try:
        with open(filename, 'w') as f:
            w = csv.DictWriter(f, fieldnames=csv_columns)
            w.writeheader()
            for data in list:
                w.writerow(data)
        f.close()
    except IOError:
        print("I/O error")

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False
    return True

if __name__ == "__main__":
    fetch_top_tracks()
