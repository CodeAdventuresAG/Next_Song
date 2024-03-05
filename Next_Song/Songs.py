import requests
import json
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image  
from random import random
import math
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Songs:
    genre = "rock"
    def __init__(self, genre = "rock"):
        self.genre = genre

    def __show(self, songname, artist, img_url):
        print("trackname: " + songname)
        print("artist: " + artist)
        try:
            ## taking img from url
            urllib.request.urlretrieve( img_url, songname+".jpg")
            
            ## saving image
            img = Image.open(songname+".jpg")
            
            ## showing image
            img.show()
            
            popularity, views = self.__Get_ratings(songname, artist)
            ## printing songname and artist
            print(f"popularity: {100 - int(popularity) + 1}")
            print(f"views: {views}")
            songname, artist, img_url, popularity, views="", "", "", "", ""
        except:
            popularity, views = self.__Get_ratings(songname, artist)
            try:
                try:
                    print(f"popularity: {100 - int(popularity) + 1}")
                    print(f"views: 0")
                except:
                    print(f"popularity: 0")
                    print(f"views: {views}")
            except:
                print(f"popularity: 0")
                print(f"views: 0")
            popularity, views="", ""
        songname, artist, img_url = "", "", ""
    def __Get_Soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')
        return soup

    def __returnRandom(self, lstordict):
        ## creating random number
        randomIndex = random()*(len(lstordict)-1)
        randomNumber = math.floor(randomIndex)        
        ## sending random number
        return randomNumber

    def random_song(self):
        
        ## scraping the website
        url = "http://www.songlyrics.com/rock-lyrics.php"
        soup = self.__Get_Soup(url)
        song_bs4 = soup.find_all('tr')
        song_info = []
        index = 0
        
        ## saving song info
        for song in song_bs4:
            songname = song.find_all('a')[-1].get_text()
            artist = song.find_all('span')[0].get_text()
            if artist == "Album":
                break
            img = song.find_all('img', {'class': 'tiny-img'})[0]['src']
            dict_song_info = {
                "songname": songname,
                "artist": artist,
                "img_url": img
            }
            
            ## appending info to the list
            song_info.append(dict_song_info)
            index += 1
            
        ## taking random song
        randomindex = self.__returnRandom(song_info)
        song = song_info[randomindex]
        
        ## returning random song
        return self.__show(song['songname'], song['artist'], song['img_url'])
    
    def Most_Popular_Song(self):
        ## taking html code
        url = "https://www.billboard.com/charts/year-end/hot-rock-songs/"
        soup = self.__Get_Soup(url)

        ## finding all the songs
        songs_details = soup.find_all("div", {"class": "o-chart-results-list-row-container"})

        ## getting info of the most popular song
        song_info = []
        for info in re.sub('[\t\n]', '$%', songs_details[0].get_text()).split('$%'):
            if info != '':
                song_info.append(info)

        ## taking the songname and artistname
        songname = song_info[1]
        artist = song_info[2]
        index = 0

        ## getting img src url
        imgs_info = soup.find_all("img", alt=True)
        for img_info in imgs_info:
            if songname.lower() in str(img_info).lower():
                break
            index += 1
        img_url = imgs_info[index]["data-lazy-src"]

        ## displaying the result
        self.__show(songname, artist, img_url)
        

    def Search_songs(self):#keyword):

        ## getting token
        client_id = "bba3cf3aeb92464d83095ebc428ba17b"
        client_secret = "35cd3d89efbb485a899e6421c89a4096"
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

        ## taking keyword
        keyword = input("Type in a keyword: ")
        (spotify.search(keyword, type="track")['tracks']['items'])
        ## searching for tracks with the keyword
        tr = spotify.search(keyword, type="track", limit=50)
        brek = False

        ## getting song list by keyword
        index = 0 
        song = []
        while brek == False:
            if index >= len(tr['tracks']['items']):
                break
            for x in range(0, len(tr['tracks']['items'][index]['artists'])):
                if "rock" in spotify.artist(tr['tracks']['items'][index]['artists'][x]['id'])['genres']:
                    song.append(tr['tracks']['items'][index])
                    break
            index += 1

        ## getting random song details
        randomindex = self.__returnRandom(song)
        song_info = song[randomindex]

        ## getting song info
        img_url = song_info['album']['images'][0]['url']
        artists = song_info['artists']
        songname = song_info['album']['name']
        artist_name = ""
        for artist in artists:
            artist_name += artist['name'] + ", "
        artist_name = artist_name[:-2]

        ## showing results
        self.__show(songname, artist_name, img_url)

    def __Get_ratings(self, songname, artist):
        try:
            client_id = "bba3cf3aeb92464d83095ebc428ba17b"
            client_secret = "35cd3d89efbb485a899e6421c89a4096"
            spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

            split_by = ":?=+"
            artist_name = re.sub("( x )|( featuring )|(,)|(&)", split_by, artist.lower()).split(split_by)

            ## returning popularity
            q = f"track:{songname} artist:{artist_name[0]}"
            tracks = (spotify.search(q, type="track")['tracks']['items'])
            artist_exists = False
            track_exists = False
            index = 0
            for track_index in range(0, len(tracks)):
                artists = tracks[track_index]['album']['artists']
                track_name = tracks[track_index]['album']['name']
                for artist_info in artists:
                    name_artist = artist_info['name']
                    if name_artist in artist:
                        artist_exists = True
                    if songname in track_name:
                        track_exists = True
                    if artist_exists and track_exists:
                        break
                    track_exists = False
                    artist_exists = False
                    index += 1

            ## returning views
            artist_to_search = ""
            if isinstance(artist_name, list) == True:
                artist_to_search = re.sub(" ", "-", artist_name[0].lower())
            else:
                artist_to_search = re.sub(" ", "-", artist_name.lower())

            songname = re.sub(" ", "-", songname.lower())
            pattern = "[,;:.!?\'\"_\/()\[\]...\n]"
            songname= re.sub(pattern, "", songname)
            artist_to_search = re.sub(pattern, "", artist_to_search)
            url = f"https://genius.com/{artist_to_search}-{songname}-lyrics"
            soup = self.__Get_Soup(url)
            views = soup.find_all("span", {"class": "LabelWithIcon__Label-sc-1ri57wg-1 kMItKF"})
            if isinstance(artist_name, list) == True:
                if len(views) == 1:
                    views = views[0].get_text()
                else:
                    views = views[-1].get_text()
            else:
                views = views.get_text()
            return tracks[index]['popularity'], views
        except:
            return 0, 0


        