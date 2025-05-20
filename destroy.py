import requests
import send_mail
import json
from github import Github
# ====== USER CONFIGURATION ======


json_file = "./content/data.json"
me = "kvsriiram2007@gmail.com"
# GitHub API endpoint for the file

GITHUB_PATH ="./content/data.json"
COMMIT_MSG = "Updated via Automatic Word Drop"


def destroy_image(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,REPO_FILE_PATH):
    COMMIT_MESSAGE = "Add image via API"

    file_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{REPO_FILE_PATH}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # Step 1: Get the file SHA
    response = requests.get(file_url, headers=headers, params={"ref": BRANCH})
    if response.status_code == 200:
        file_info = response.json()
        file_sha = file_info["sha"]
        #print("File SHA:", file_sha)
    else:
        print("File not found or error fetching file info.")
        print("Response:", response.json())
        send_mail.mail(me,me,"Error - destroy.py",str(response.json()))

        exit(1)

    # Step 2: Delete the file
    delete_payload = {
        "message": COMMIT_MESSAGE,
        "sha": file_sha,
        "branch": BRANCH
    }

    delete_response = requests.delete(file_url, json=delete_payload, headers=headers)
    if delete_response.status_code == 200:
        print("\n✅ File deleted successfully!")
        #print("GitHub API response:", delete_response.json())
    else:
        print("\n❌ Failed to delete the file.")
        #print("Status code:", delete_response.status_code)
        #print("Response:", delete_response.json())
        send_mail.mail(me,me,"Error - destroy.py",str(delete_response.json())+"\n\n"+str(delete_response.status_code))


def pop_json(GITHUB_TOKEN,REPO_OWNER,REPO_NAME,BRANCH,GITHUB_PATH):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list) and data:
        popped = data.pop(0)
        print("Removed:", popped)
    else:
        print("data.json is not a non-empty list.")
        return
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 2. Authenticate and get repo
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_OWNER+"/"+REPO_NAME)
    file_content = repo.get_contents(GITHUB_PATH)
    
    # 3. Read the updated local file and encode it
    with open(json_file, 'rb') as f:
        content_bytes = f.read()
    
    # 4. Commit the updated file to GitHub
    repo.update_file(
        path=GITHUB_PATH,
        message=COMMIT_MSG,
        content=content_bytes,
        sha=file_content.sha,
        branch=BRANCH
    )
    print("Committed changes to GitHub.")

