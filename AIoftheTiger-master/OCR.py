from __future__ import print_function
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client import tools


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\HP\\Documents\\AIoftheTiger\\credentials (1).json"

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
DOC_SCOPE = ['https://www.googleapis.com/auth/documents']
CLIENTSECRET = 'credentials.json'
APPNAME = 'Drive API Python Quickstart'

def prepare_ocr():
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)
    doc_service = build('docs', 'v1', credentials=creds)
    return creds, drive_service, doc_service



def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENTSECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


# need to get picture uploaded to the google drive, open with google docs and grab this info above (automate this process)
def upload_to_drive(path, filename, creds=None, drive_service=None, doc_service=None):
    # # uploads a file to the root folder of the google drive
    # file_id = deprecated_drive_service.upload_file('Test1IMG', 'C:\\Users\\HP\\Documents\\AI Frames\\TW3.jpg', "root",
    #                                  mime_type='image/jpeg')
    #
    # print(file_id)

    if creds  == None:
        # get the credentials to access this application
        creds = get_credentials()

    if drive_service == None:
        # create object to access google drive
        drive_service = build('drive', 'v3', credentials=creds)

    # File's new metadata.
    mime_type = 'application/vnd.google-apps.document'

    # File's metadata
    file_metadata = {
        'name': filename,
        'mimeType': mime_type
    }

    # initialize media
    media = MediaFileUpload(path,
                            mimetype='image/jpeg',
                            resumable=True)

    # create the file initialized with the above file data & store the file object
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    # print('File ID: %s' % file["id"])

    if doc_service == None:
        # create an object to access google docs
        doc_service = build('docs', 'v1', credentials=creds)

    #store the doc object we are trying to access
    document = doc_service.documents().get(documentId=file['id']).execute()

    text_str = ''

    # grab the text from a file by line & output it on the console
    for x in range(0, len(document.get('body').get('content'))):
        try:
            # print('{}'.format(document.get('body').get('content')[x]['paragraph']['elements'][0]['textRun']['content']))
            text_str += '{}'.format(document.get('body').get('content')[x]['paragraph']['elements'][0]['textRun']['content'])
        except:
            continue

    drive_service.files().delete(fileId=file['id']).execute()

    return text_str

def find_tiger(output_txt):
    output_txt = output_txt.upper()
    str_to_check = ["TIGER", "WOODS"]
    for string in range(0,len(str_to_check)):
        tiger = output_txt.find(str_to_check[string])
        if tiger >= 0:
            tiger = True
            return tiger
    return False


# upload an image to the google drive
# call the ocr function on google drive
# grab the text and decipher if it contains "tiger woods" and similar phrases
def main_ocr(path, filename, creds=None, drive_service=None, doc_service=None):
    # filename = 'frame50444'
    # path = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\2008_U.S._Open_Final_Round_Full_Telecast-Vvi_LtvptKs Folder\\" + filename + '.jpg'
    output_txt = upload_to_drive(path, filename, creds, drive_service, doc_service)
    tiger = find_tiger(output_txt)
    return tiger


if __name__ == '__main__':
    main_ocr("a","b")