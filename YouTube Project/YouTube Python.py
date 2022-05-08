from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
#%%
API_KEY='AIzaSyBM7Jk33DIvtnYCVc-2tlAxpYmZ0Crb9p8'
#%%
chanels_id=["UCJQJAI7IjbLcpsjWdSzYz0Q",
            "UCnz-ZXXER4jOvuED5trXfEA",
            "UCLLw7jmFsvfIVaUFsLs8mlQ",
            "UCWv7vMbMWH4-V0ZXdmDpPBA",
            "UCiT9RITQ9PW6BhXK0y2jaeg",
            "UCCezIgC97PvUuR4_gbFUs5g",
            'UC2UXDak6o7rBm23k3Vv5dww'
            'UC7cs8q-gJRlGwj4A8OmCmXg'
            "UCTs3VX60I6EKrrwdkgrwCGQ"
            ]
#%%
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
#%%
youtube = build(
        api_service_name, api_version, developerKey=API_KEY)


def get_chanels_id(youtube,chanels_id):
        Data_List=[]
        request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=','.join(chanels_id
                            )
        )
        response = request.execute()
        for i in range(len(response['items'])):
            data = dict(Channel_name = response['items'][i]['snippet']['title'],
                        Chanel_id=response['items'][i]['id'],
                        playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                        Subscribers =response['items'][i]['statistics']['subscriberCount'],
                        Videos =response['items'][i]['statistics']['videoCount'],
                        views=response['items'][i]['statistics']['viewCount'],

                        # likes=response['items'][i]['contentDetails']['likes']
                        )
            Data_List.append(data)
        return Data_List
#%%
get_chanels_id(youtube,chanels_id)
#%%
df=pd.DataFrame(get_chanels_id(youtube,chanels_id))


#%%
df.dtypes
#%%
for i in df.columns[3:]: df[i] = pd.to_numeric(df[i])
df.dtypes

def get_videos_id(youtube,playlist_id):
    videos_id=[]
    request = youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,
                                               maxResults=50)
    response = request.execute()
    # for i in range(len(response['items'])):
    #     videos_id.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request = youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,
                                               maxResults=50,
                                               pageToken=next_page_token)

            response = request.execute()

            for i in range(len(response['items'])):
                videos_id.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')

    return videos_id





playlists_id=[]
for i in df["Channel_name"]:
        playlist=df.loc[df['Channel_name']==i,'playlist_id'].iloc[0]
        playlists_id.append(playlist)




videos_list=get_videos_id(youtube,playlists_id[2]) #mosh


def get_video_details(youtube,videos_list):
    all_videos_statistics=[]
    for i in range(0,len(videos_list),50):
        request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join( videos_list[i:i+50]  ##maximum 50 ids
        ))
        response = request.execute()


        for video in response['items']:
            video_stats = dict(Title=video['snippet']['title'],
                               published_date=video['snippet']['publishedAt'],
                               views=video['statistics']['viewCount'],
                               likes=video['statistics']['likeCount'],
                               # dislikes=video['statistics']['dislikeCount'],
                               comments=video['statistics']['commentCount']
                               )
            all_videos_statistics.append(video_stats)

    return all_videos_statistics

video_data=get_video_details(youtube,videos_list)

df_videos=pd.DataFrame(video_data)
