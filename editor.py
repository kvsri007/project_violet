from page_1 import *
from page_2 import *
import upload
import destroy
import publish_content
import send_mail
import os
import time

## SECRET ##

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
IG_ACCESS_TOKEN = os.getenv("IG_TOKEN")
IG_USER_ID = os.getenv("IG_ID")

############


REPO_OWNER = "kvsri007"         
REPO_NAME = "project_violet"                      
BRANCH = "main"                              
LOCAL_IMAGE_PATH = "./content/"   
REPO_IMAGE_PATH = "content/"         
direct_links = []
GITHUB_PATH = "./content/data.json"
me = "kvsriiram2007@gmail.com"


def generate_post(WORD,IPA,DEFINITION,EXAMPLE_1,EXAMPLE_2):
    try:
        print("content sent to editor")
        gen_page1("./assets/t_one.png",WORD,IPA,"./content/1.jpg")
        gen_page2("./assets/t_two.png","Definition",DEFINITION,"","./content/2.jpg")
        gen_page2("./assets/t_three.png","Examples",EXAMPLE_1,EXAMPLE_2,"./content/3.jpg")
        print("Generated Succefully ")
        try :
            for i in range(1,4):
                
                url = upload.upload_img(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,LOCAL_IMAGE_PATH+str(i)+".jpg",REPO_IMAGE_PATH+WORD+"_"+str(i)+".jpg")
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


