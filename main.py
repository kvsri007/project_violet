
import upload
import destroy
import editor
import publish_content
import json
import send_mail
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory where your script is
ASSET_DIR = os.path.join(BASE_DIR, "assets")
CONTENT_DIR = os.path.join(BASE_DIR, "content")

json_file = os.path.join(CONTENT_DIR, "data.json")
me = "kvsriiram2007@gmail.com"


def get_content(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

   
    values = list(data[0].values())
    return values

try:
    
    content = get_content(json_file)
    print("content extracted")
    print(content)
    editor.generate_post(content[1],content[2],content[3],content[4],content[5])
    send_mail.mail(me,me,"Success","Posted")

except Exception as e:
    send_mail.mail(me,me,"Error - main.py",str(e))
