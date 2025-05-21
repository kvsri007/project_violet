import requests
import time
import upload
import send_mail
import json
import random
import os
me = "kvsriiram2007@gmail.com"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory where your script is
ASSET_DIR = os.path.join(BASE_DIR, "assets")
CONTENT_DIR = os.path.join(BASE_DIR, "content")

json_file = os.path.join(CONTENT_DIR, "data.json")

caption_file = os.path.join(CONTENT_DIR, "caption.txt")
tags_raw = ['#Vocabulary', '#WordOfTheDay', '#LearnNewWords', '#Automation', '#PythonProgramming', '#TechAutomation', '#CodingLife', '#TechPortfolio', '#APIs', '#WorkflowAutomation', '#InstagramAutomation', '#ContentAutomation', '#SocialMediaAutomation', '#InstagramWorkflow', '#ContentCreator', '#InstaCarousel', '#LearnWithMe', '#StayCurious', '#TechCommunity', '#Innovation', '#CreativeTech', '#TechJourney', '#BuildInPublic', '#DailyVocabulary', '#EnglishVocabulary', '#WordNerd', '#LanguageLearning', '#ContentCreation', '#SocialMediaTips', '#TechProjects']
default_tag = "#AutomaticWordDrop "



def generate_caption(file,count):
    tags_selected = random.sample(tags_raw,10)
    tags = " ".join(tags_selected)
    
    line_1 = f"🚀 Day {count} - #1 Automatic Word Drop — from Project Violet"
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()
        
        return line_1 + "\n\n" + content + "\n\n\n\n\n\n\n\n\n\n" + default_tag + tags 


def get_content(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    values = list(data[0].values())
    return values


def create_media_container(ACCESS_TOKEN,IG_USER_ID,image_url):
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "image_url": image_url,
        "is_carousel_item": True,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, json=payload)
    data = res.json()
    if "id" in data:
        return data["id"]
    else:
        print("Error creating media container:", data)
        return None

def create_carousel_container(ACCESS_TOKEN,IG_USER_ID,children_ids, caption):
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "media_type": "CAROUSEL",
        "children": children_ids,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, json=payload)
    data = res.json()
    if "id" in data:
        return data["id"]
    else:
        print("Error creating carousel container:", data)
        return None

def publish_carousel(ACCESS_TOKEN,IG_USER_ID,creation_id):
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, json=payload)
    data = res.json()
    print("Publish response:", data)
    return data


def post_carousel(ACCESS_TOKEN,IG_USER_ID,IMAGE_URLS):
    try:

        print(IMAGE_URLS,"\n\nPOSTING\n\n")
        time.sleep(10)
       
        print(IMAGE_URLS,"\n\nWait...\n\n")
        container_ids = []
        for img_url in IMAGE_URLS:
            media_id = create_media_container(ACCESS_TOKEN,IG_USER_ID,img_url)
            if media_id:
                container_ids.append(media_id)
            time.sleep(2)  

        if len(container_ids) != len(IMAGE_URLS):
            print("Failed to create all media containers. Exiting.")
            exit(1)

       
        caption = generate_caption(caption_file,str(int(get_content(json_file)[0])))
        carousel_id = create_carousel_container(ACCESS_TOKEN,IG_USER_ID,container_ids,caption)
        if not carousel_id:
            print("Failed to create carousel container. Exiting.")
            exit(1)

        publish_carousel(ACCESS_TOKEN, IG_USER_ID, carousel_id)
        
        print("POSTED")
    
    except Exception as e:
        send_mail.mail(me,me,"Error - publish_content.py",str(e))
