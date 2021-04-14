import json
import requests
from secrets import spotify_user_id, spotify_token, discover_weekly_id
from datetime import date

class saveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):
        # Loop through playlist tracks and add tyhem to list
        print("Finding songs in discover weekly...")
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)

        response = requests.get(query,
        headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)})


        #what we get back is a json list
        response_json = response.json()
        print(response)

        #now we want to create a list of individual ids
        #use for loop
        #need to break down the json even further
        #we want to extract URI of each spotify song in the playlist
        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.addSongsToPlaylist()

        #print(i["track"]["uri"])
        #print(self.tracks)

    def create_playlist(self):
        # Create a new playlist
        today = date.today()
        todayFormatted = today.strftime("%d/%m/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        #Now we need to specify the body of the query
        request_body = json.dumps({
            "name": todayFormatted + " Discover Weekly",
            "description": "weekly updated discover weekly dumped into 1 playlist",
            "public": True
        })

        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)})

        response_json = response.json()
        print(response_json)

        return response_json["id"]

    def addSongsToPlaylist(self):
        #add all songs to new playlist
        print("Adding Songs...")

        self.new_playlist_id = self.create_playlist()

        #query: you need playlist id, and comma separated list of spotify URIs to add to the playlist
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        response = requests.post(query, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)})

        print(response.json)



a = saveSongs()
a.find_songs()


