import json
import requests

class Spotify:
    def __init__(self):
        self.apikey = "Cu91oiwbrhN3kPtddgGpcB0lWjH8XkG8"
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

        for item in json.loads(a.artist_data)['albums']["items"]:
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
        return self.artist_data

    def get_album(self,album_id):
        url = self.base_url + f"albums?ids={album_id}"

        self.query(url)
        return self.query(url)

    def get_all_albums(self):
        return self.album_list

a = Spotify()
user_artist = input("Please enter a artist name: ")
a.search(user_artist)
# print(a.search())

# print(a.name)
# print(a.album_list)

user_album = input("Please type album name of artist: ").lower()
for i in a.album_list:
    print(i["name"])
    if user_album == i["name"].lower():
        print(i["id"])
    