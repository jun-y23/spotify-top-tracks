# main script fetch top tracks
import settings
import json
import requests
import csv

token = settings.TOKEN
token_endpoint = 'https://accounts.spotify.com/api/token'
payload = {'grant_type': 'client_credentials'}
headers = {'Authorization': 'Basic {}'.format(token)}

bz_id = '7i9bNUSGORP5MIgrii3cJc'
top_tracks_endpoint = 'https://api.spotify.com/v1/artists/{}/top-tracks?market=JP'.format(bz_id)

top_ten_track_list = []


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


csv_columns = ['name', 'popularity', 'uri']
def write_csv(list):
    try:
        with open('bz.csv', 'w') as f:
            w = csv.DictWriter(f, fieldnames=csv_columns)
            w.writeheader()
            for data in list:
                w.writerow(data)
        f.close()
    except IOError:
        print("I/O error")

fetch_top_tracks()
