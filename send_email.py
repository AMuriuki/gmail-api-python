from ast import parse
import os


# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachment MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from base import gmail_authenticate, email_address, recipients


def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    fp = open(filename, 'rb')
    if main_type == 'text':
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
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


def build_message(destination, obj, body, attachments=[]):
    if not attachments:
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = email_address
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = email_address
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
        userId="me",
        body=build_message(destination, obj, body, attachments)
    ).execute()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Email Sender using Gmail API")
    parser.add_argument("subject", type=str, help="The subject of the email")
    parser.add_argument("body", type=str, help="The body of the email")
    parser.add_argument("-f", "--files", type=str,
                        help='Email attachments', nargs="+")

    args = parser.parse_args()

    # get the Gmail API service
    service = gmail_authenticate()
    send_message(service, recipients, args.subject, args.body, args.files)
