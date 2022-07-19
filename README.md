## Table of contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Setup](#setup)

## Introduction
This project helps you download all your saved post(videos) on reddit.

## Technologies
Project is created with:
* Python
* ffmpeg

## Make sure you have ffmpeg downloaded for this to work.

## Setup
1. Clone this reposetory in any folder of your device

2. To run this project you first need to register yourself on reddit api(very-easy)
[Reddit-Api](https://www.reddit.com/prefs/apps)

Guide to register on Reddit Api: [Blog](https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)

3. Fill out your credentials in credentials.py
```
client_id= "YOUR CLIENT ID HERE"
client_secret= "YOUR CLIENT SECRET HERE"
user_agent= "Agent_L" #You can leave this be
username= "YOUR REDDIT USER NAME HERE"
password= "YOUR REDDIT PASSWORD HERE"
```

4. Now just run the python file 

##### **Note that the post gets unsaved after it's downloaded(You can change it though)**

