import os
import random
import string
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Playlist,YouTube,Search
import tkinter as tk
from tkinter import filedialog

#  problem with youtube downloadr 



load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def spotify_credentials(client_id,client_secret):
          ''' using SpotifyClientCredentials to get access to Spotify API '''
          #   call function to get the client id and secret---------------------------------------------------------------------------------
          client_credential_manager=SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
          return spotipy.Spotify(client_credentials_manager=client_credential_manager)


# ---------------------------------------------  url of the playlist user wants to download
playlist_url="https://open.spotify.com/playlist/29bZkP608NjxuvEdZVVkJK"


#----------------------------------------------------storing credentials in session
session=spotify_credentials(client_id,client_secret)


def playlist_tracks_extractor(playlist_url):
    ''' get list of tracks in a given playlist (note: max playlist length 100)'''
    tracks = session.playlist_tracks(playlist_url)["items"]
    songs=[]
    for track in tracks:
           artists=''
           for artist in track["track"]["artists"]:
                  artists=artists + artist["name"] + ", "
           artists=artists[:-2]
           songs.append(track["track"]["name"] + " by " + artists)

    return songs



def download_quality_choice():
    ''' downloading quality of the video '''
    options = {
              'High': 1,
              'Medium': 2,
              'Low': 3
    }

    print("Select the quality")
    for i in options:
        print(i)
    choice = input("Enter your choice : ")
    choice=choice.capitalize()

    return options[choice]



def select_download_directory():
    ''' Open a dialog to select the download directory '''
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    download_dir = filedialog.askdirectory(title="Select Download Directory")
    return download_dir

def download_quality_song(stream_list,choice):
      abr_values=[steam.abr for steam in stream_list]
      abr_values=[int(x[:-4]) for x in abr_values if int(x[:-4])]
      abr_values=sorted(abr_values)
      print(abr_values)
      if choice==1:
            return abr_values[-1]
      elif choice==2:
            return abr_values[random.randint(1, len(abr_values) - 2)]
      elif choice==3:
            return abr_values[0]
      



def download_quality_video(stream_list,choice):
      # stream object has atttribute resolutin insted of res which is pritned as property in terminal
      res_values = [int(stream.resolution[:-1]) for stream in stream_list if stream.resolution[:-1] is not None ]
      print(res_values)
      res_values=set(res_values)
      res_values = list(res_values)
      res_values = sorted(res_values)
      print(res_values)
      if not res_values:
        return None
      if choice==1:
            return res_values[-1]
      elif choice==2:
            return res_values[random.randint(1, len(res_values) - 2)]
      elif choice==3:
            return res_values[0]


def search_song_file(songs,download_dir):
      choice=download_quality_choice()
      for song in songs:
            search = Search(song)
            stream = search.results[0].streams.filter(only_audio=True)
            stream_quality=download_quality_song(stream,choice)
            stream_quality=str(stream_quality)+'kbps'
            stream=stream.filter(abr=stream_quality).first()
            #  invalid character in file name ie sonf name with  artist can break the function
            if stream:
                  file_path = os.path.join(download_dir, f'{song}.mp3')
                  #stream.download(output_path=download_dir, filename=f'{song}.mp3')
                  print(f'Downloaded: {file_path}')
            else:
                  print(f'No stream found for {song} in {stream_quality}')


# little refining need to be done
def search_video_file(videos,download_dir):
      choice=download_quality_choice()
      for video in videos:
            search = Search(video)
            stream = search.results[0].streams.filter(only_video=True)
            print(stream)
            stream_quality_res=download_quality_video(stream,choice)
            print(stream_quality_res)
            if stream_quality_res is None:
                  continue
            stream_quality=str(stream_quality_res)+'p'
            stream=stream.filter(resolution=stream_quality_res).first()
            print(stream)
            #  invalid character in file name ie sonf name with  artist can break the function
            if stream:
                  file_path = os.path.join(download_dir, f'{video}.mp4')
                  #stream.download(output_path=download_dir, filename=f'{video}.mp4')
                  print(f'Downloaded: {file_path}')
            else:
                  print(f'No stream found for {video} in {stream_quality}')
'''
=========================================================================================
'''

#playlist_tracks_extractor(playlist_url)
#print(download_quality())
#print(search_stream_file(playlist_tracks_extractor(playlist_url)))

if __name__ == "__main__":
    playlist_tracks = playlist_tracks_extractor(playlist_url)
    download_dir = select_download_directory()
    
    if download_dir:
        search_song_file(playlist_tracks, download_dir)
    else:
        print("Download directory selection canceled.")

