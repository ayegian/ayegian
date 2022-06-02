from __future__ import print_function
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import subprocess

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    threads = service.users().threads().list(userId = "me").execute().get('threads', [])
    for id in threads:
        flag = False

        thread = service.users().threads().get(userId = "me", id = id['id']).execute()
        msgid = (thread['messages'][0]['id'])
        message = service.users().messages().get(userId = "me", id = msgid).execute()
        headers = message['payload']['headers']
        for header in headers:
            if(header['name'] == 'Subject' and header['value']=='test'):
                body = message['payload']
                attachment = 0
                try:
                    body = message['payload']['parts'][0]['parts'][0]['body']['data']
                    attachmentID = message['payload']['parts'][1]['body']['attachmentId']
                except:
                    break
                print(attachmentID)
                print(type(body))
                print(body)
                body = base64.b64decode(body)
                body = bytes.decode(body)
                body = body.strip()
                print(type(body))
                print(body)
                chunks = body.split(',')
                print(chunks[0])
                for x in body:
                    print(x,"\n")
                flag = True
                name_chunks = chunks[0].split(' ')
                csv_path = 'D:/pass_folder/input/'+name_chunks[0]+'_'+name_chunks[1]+'.csv'
                with open(csv_path, 'w') as file:
                    file.write(body)
                attachment = service.users().messages().attachments().get(userId = "me", messageId = msgid, id = attachmentID).execute()['data']
                #attachment = base64.urlsafe_b64decode(attachment)
                #attachment = base64.urlsafe_b64decode(attachment.encode('UTF-8'))
                attachment_data = base64.urlsafe_b64decode(attachment.encode('UTF-8'))
                png_path = 'D:/pass_folder/input/'+chunks[0]+'.png'
                with open(png_path, 'wb') as f:
                    f.write(attachment_data)


                break
        if(flag):
          break
    #Call the Gmail API
    

if __name__ == '__main__':
    main()
    subprocess.Popen(["D:/pass_folder/command/run_passes.bat", "ayegian@gmail.com"])