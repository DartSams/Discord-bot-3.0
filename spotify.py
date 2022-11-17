import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Spotify:
    def __init__(self):
        self.apikey = os.getenv('spotify_api_key')
        self.headers = {
            "apikey":self.apikey
        }
        self.base_url = "https://api.apilayer.com/spotify/"
        self.artist_data = {}
        self.album_list = []

    def query(self,url):
        response = requests.request("GET", url, headers=self.headers)
        result = response.text
        return result

    def search(self,name):
        self.name = name.replace(" ","%20")
        url = self.base_url + f"search?q={self.name}"

        self.artist_data = self.query(url)
        profile = {}
        artist = json.loads(self.artist_data)['artists']["items"][0]
        profile["name"] = artist["data"]["profile"]["name"]
        profile["pic"] = artist["data"]["visuals"]["avatarImage"]["sources"][0]["url"]

        self.get_all_albums()
        return profile

    def get_all_albums(self):
        for item in json.loads(self.artist_data)['albums']["items"]:
            all_album_data = item["data"]
            # print(item["data"])
            # print(item["data"]["uri"])
            album_uri = item["data"]["uri"].split(":")
            album_id = album_uri[-1]
            # print(album_id)
            album_name = item["data"]["name"]
            album = {
                "name":album_name,
                "id":album_id
            }

            self.album_list.append(album)
        return self.album_list

    def get_artist_album(self,artist_name:str=None,album_name:str=None):
        if album_name:
            artist = self.search(artist_name)
            data = {}
            for i in self.album_list:
                # print(i["name"])
                if album_name.lower() == i["name"].lower():
                    # print(i["id"])
                    album = self.get_album(i["id"])
                    data["artist"] = artist
                    data["album"] = album
                    return data
        return self.search(artist_name)

    def get_album(self,album_id):
        url = self.base_url + f"albums?ids={album_id}"

        album = self.query(url)
        album_data = {}
        for item in json.loads(album)["albums"]:
            # print(item)
            url = item["external_urls"]["spotify"]
            # print(url)
            release_date_data = item["release_date"].split("-")
            release_date = f"{release_date_data[1]} {release_date_data[2]}, {release_date_data[0]}"

            album_data["album_url"] = url
            album_data["release_date"] = release_date
        return album_data

##place this block when discord message is .sp artist Ex. .sp kota the friend
a = Spotify()
# user_artist = input("Please enter a artist name: ")
# # a.search(user_artist)
# print(a.search(user_artist))

# # # print(a.name)
# # # print(a.album_list)

# # ##place this block when discord message is .sp artist album name Ex. .sp kota the friend everything
# user_album = input("Please type album name of artist: ").lower()
# for i in a.album_list:
#     # print(i["name"])
#     if user_album == i["name"].lower():
#         print(i["id"])


# print(a.get_album("0cMxALtiABnT1kIuA1wgsQ"))
    

print(a.get_artist_album("kota the friend","everything"))