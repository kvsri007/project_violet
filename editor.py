from page_1 import *
from page_2 import *
import upload
import destroy
import publish_content
import send_mail
import os
import time

## SECRET ##

GITHUB_TOKEN = os.getenv("G_TOKEN")
IG_ACCESS_TOKEN = os.getenv("IG_TOKEN")
IG_USER_ID = os.getenv("IG_ID")

############


REPO_OWNER = "kvsri007"         
REPO_NAME = "project_violet"                      
BRANCH = "main"                              
#LOCAL_IMAGE_PATH = "./content/"   
REPO_IMAGE_PATH = "content/"         
direct_links = []
GITHUB_PATH = "./content/data.json"
me = "kvsriiram2007@gmail.com"

######


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory where your script is
ASSET_DIR = os.path.join(BASE_DIR, "assets")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
# Font paths
FONT_BOLD = os.path.join(ASSET_DIR, "timesbd.ttf")
FONT_BOLD_ITALIC = os.path.join(ASSET_DIR, "timesbi.ttf")
FONT_ITALIC = os.path.join(ASSET_DIR, "timesi.ttf")

# Template paths
TEMPLATE_ONE = os.path.join(ASSET_DIR, "t_one.png")
TEMPLATE_TWO = os.path.join(ASSET_DIR, "t_two.png")
TEMPLATE_THREE = os.path.join(ASSET_DIR, "t_three.png")

CONTENT_ONE = os.path.join(CONTENT_DIR, "1.jpg")
CONTENT_TWO = os.path.join(CONTENT_DIR, "2.jpg")
CONTENT_THREE = os.path.join(CONTENT_DIR, "3.jpg")

def generate_post(WORD,IPA,DEFINITION,EXAMPLE_1,EXAMPLE_2):
    try:
        print("content sent to editor")
        gen_page1(TEMPLATE_ONE,WORD,IPA,CONTENT_ONE)
        gen_page2(TEMPLATE_TWO,"Definition",DEFINITION,"",CONTENT_TWO)
        gen_page2(TEMPLATE_THREE,"Examples",EXAMPLE_1,EXAMPLE_2,CONTENT_THREE)
        print("Generated Succefully ")
        try :
            for i in range(1,4):
                
                url = upload.upload_img(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,os.path.join(CONTENT_DIR,str(i)+".jpg"),REPO_IMAGE_PATH+WORD+"_"+str(i)+".jpg")
                direct_links.append(url)
                time.sleep(1)


            publish_content.post_carousel(IG_ACCESS_TOKEN,IG_USER_ID,direct_links)
            
            for i in range(1,4):
                destroy.destroy_image(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,REPO_IMAGE_PATH+WORD+"_"+str(i)+".jpg")
                time.sleep(1)

            destroy.pop_json(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,GITHUB_PATH)
        except Exception as e:
            send_mail.mail(me,me,"Error - editor.py",str(e))  

    except Exception as e:
        send_mail.mail(me,me,"Error - editor.py",str(e))
