import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email(service, sender, to, subject, body):
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject


    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(f"Message Id: {send_message['id']}")

def mail(sender,to,subject,body ):
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    send_email(service, sender, to, subject, body)

