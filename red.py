from logging import exception
import praw

import os
import time
import datetime
from credentials import *

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)


def is_video(post):
    """
    Returns True if the post is a video and is posted on reddit and reddit only (no gyfcat) 
    """
    url = post.url
    url = url.lower()
    points = 0
    Non_Video_extensions = [".JPG", "gfycat", ".GIF", ".JPE", ".BMP", ".PNG", "jpeg"]
    
    for item in Non_Video_extensions:
        item = item.lower()
        if item not in url:
            points += 1
        else:
            return False
    if points == 7:
        return True
    
def go_download(post, foldername):
    """
    > Gives error if the post is a forwarded post

    All the things this function does:
    > Updates Discription accordingly
    > Downloades given video with or without sound
    > Organizes the video in particular folder
    > Replace the discription in the same folder as it's respective video
    """
    import os, requests
    global description
    print(post.url)
    os.makedirs(foldername, exist_ok=True)


    permalink = post.permalink
    url = "https://www.reddit.com"+permalink
    json_url = url[:-1]+".json"

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

    r = requests.get(json_url, headers={"User-agent":user_agent})
    data = r.json()[0]


    try:
        video_url = data["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]
        audio_url = "https://v.redd.it/"+video_url.split("/")[3]+"/DASH_audio.mp4"
    except exception as e:
        print("A shared post was detected. Ignoring and and moving forward")
        return


    with open("video.mp4", "wb") as f:
        g = requests.get(video_url, stream=True)
        f.write(g.content)

    with open("audio.mp3", "wb") as f:
        g = requests.get(audio_url, stream=True)
        f.write(g.content)

    try:
        os.system(f"ffmpeg -i video.mp4 -i audio.mp3 -c copy -y {post.id}.mp4")

        os.remove("audio.mp3")
        os.rename(fr"{post.id}.mp4", fr"{foldername}/{post.title[:10]}.mp4")
        os.remove("video.mp4") 

    except:
        print("Audio was not found. Saving without audio...")
        os.rename(fr"video.mp4", fr"{foldername}/{post.title[:10]}.mp4")
    
    description += f"This video was posted by u/{post.author} on {datetime.datetime.fromtimestamp(int(post.created_utc)).strftime('%Y-%m-%d %H:%M:%S')} on r/{post.subreddit} \nPlease Comment for Removal or Credits \nHave a nice day\n"
    with open("description.txt", "w") as f:
        f.write(description)
    os.rename(fr"description.txt", fr"{foldername}/{post.title[:10]}.txt")
    
i = 1
for post in reddit.user.me().saved(limit=None):
    if is_video(post):
        print(f"Video Count: {i}")
        i += 1
        description = ""
        Title = f"Title: {post.title}\n"
        description += f"{Title}Description: "
        os.makedirs(f"{post.subreddit}", exist_ok=True)
        go_download(post, f"{post.subreddit}")
        post.unsave()