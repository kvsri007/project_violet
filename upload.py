import requests
import base64
import os
import send_mail

me = "kvsriiram2007@gmail.com"


REPO_OWNER = "kvsri007"         
REPO_NAME = "project_violet"                   
BRANCH = "main"


def upload_img(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,LOCAL_IMAGE_PATH,REPO_IMAGE_PATH):
    try:

        COMMIT_MESSAGE = "Uploaded by Automatic Word Drop"
        if not os.path.isfile(LOCAL_IMAGE_PATH):
            print(f"File not found: {LOCAL_IMAGE_PATH}")
            exit(1)


        with open(LOCAL_IMAGE_PATH, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

      
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{REPO_IMAGE_PATH}"


        payload = {
            "message": COMMIT_MESSAGE,
            "content": encoded_string,
            "branch": BRANCH
        }


        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }


        response = requests.put(url, json=payload, headers=headers)
        result = response.json()



        if "content" in result and "path" in result["content"]:
            direct_link = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{REPO_IMAGE_PATH}"
            print("\n✅ Upload successful!")

            return direct_link
        else:

            if "message" in result:
                send_mail.mail(me,me,"Error - upload.py",result["message"])
                print("Error:", result["message"])
            else:
                print("Unknown error. See API response above.")
                send_mail.mail(me,me,"Error - upload.py","Unkown error")
    except Exception as e:
        print(e)

