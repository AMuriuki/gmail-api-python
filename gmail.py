import os
import pickle

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachment MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from decouple import config

# Request all access (permission to read/send/receive emails & manage inbox and more)
SCOPES = ['https://mail.google.com/']
email_address = config('email_address')


def gmail_authenticate():
    creds = None
    # token.pickle stores user access and refreshes tokens
    # this file is created automatically
    # after the authorization flow completes for the 1st time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # if no valid credentials available, allow user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # save credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


# get the Gmail API service
service = gmail_authenticate()

# Add attachment to email
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    fp = open(filename, 'rb')
    if main_type == 'text':
        msg = MIMEText(fp.read(), _subtype=sub_type)
    elif main_type == 'image':
        msg = MIMEImage(fp.read(), _subtype=sub_type)
    elif main_type == 'audio':
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
    else:
        msg = MIMEBase(main_type, sub_type)
    fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
