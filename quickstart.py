from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from google.cloud import vision
from googleapiclient.http import MediaFileUpload
from pygdrive3 import service
import js2py

from importlib_metadata.docs.conf import language

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "C:\\Users\\HP\\Documents\\AIoftheTiger\\client_secret.json"
import os
from google.oauth2 import service_account

#credentials = service_account.Credentials.from_service_account_file(client_email="dwash2016@gmail.com", token_uri= "", "C:\\Users\\HP\\Documents\\AIoftheTiger\\credentials.json")
# client = language.LanguageServiceClient(credential ps=credentials)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '16AE48VOWPKRRB8Gma49q_vnCs7rDZ3McdG-AYCH49hQ'

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


# from googleapiclient import errors
# from googleapiclient.http import MediaFileUpload
# # ...
#
# def insert_file(service, title, description, parent_id, mime_type, filename):
#   """Insert new file.
#
#   Args:
#     service: Drive API service instance.
#     title: Title of the file to insert, including the extension.
#     description: Description of the file to insert.
#     parent_id: Parent folder's ID.
#     mime_type: MIME type of the file to insert.
#     filename: Filename of the file to insert.
#   Returns:
#     Inserted file metadata if successful, None otherwise.
#   """
#   media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
#   body = {
#     'title': title,
#     'description': description,
#     'mimeType': mime_type
#   }
#   # Set the parent folder.
#   if parent_id:
#     body['parents'] = [{'id': parent_id}]
#
#   try:
#     file = service.files().insert(
#         body=body,
#         media_body=media_body).execute()
#
#     # Uncomment the following line to print the File ID
#     # print 'File ID: %s' % file['id']
#
#     return file
#   except errors.HttpError as error:
#     print ('An error occurred: %s')
#    return None


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
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
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)


    title = 'My Document'
    body = {
        'title': title,
        #'content': "Json"
        #'content': #image that is uploaded on the drive
        }
   # doc = service.documents().create(body=body).execute()
  #  print('Created document with title: {}'.format(
   #     doc.get('title')))
    # upload and convert to google doc
    #PREVIOUSLY MYFOLDER
    #DOCUMENT_ID = "13vtNm6i6KLTwkT-XrFX1sKA5iV2a_jm0"
    #file_to_gd_docs(service, myFolder)

    upload_to_drive()

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    # grab the text from a file by line
    for x in range(0, len(document.get('body').get('content'))):
        try:
            print('{}'.format(document.get('body').get('content')[x]['paragraph']['elements'][0]['textRun']['content']))
            print(x)
        except:
            continue




def file_to_gd_docs( service2, import_file=None):
    #authorization part(success)
    # drive_service = service.DriveService("C:\\Users\\HP\\Documents\\AIoftheTiger\\credentials.json")
    # credentials = drive_service.auth()
    # service2 = build('docs', 'v1', credentials=credentials)

    title = 'My Document'
    body = {
        'title': title
    }
    doc = service2.documents().create(body=import_file).execute()
    print('Created document with title: {0}'.format(
        doc.get('title')))







# need to get picture uploaded to the google drive, open with google docs and grab this info above (automate this process)
def upload_to_drive():
    file_metadata = {'name': 'TW3.jpg'}
    media = MediaFileUpload('C:\\Users\\HP\\Documents\\AI Frames\\TW3.jpg', mimetype='image/jpeg')
    drive_service = service.DriveService("C:\\Users\\HP\\Documents\\AIoftheTiger\\credentials (1).json")
    drive_service.auth()
    # file = drive_service.files().create(body=file_metadata,
    #                                     media_body=media,
    #                                     fields='id').execute()


    folder = drive_service.create_folder('Test3')
    print(folder)
    drive_service.upload_file('Test1IMG', 'C:\\Users\\HP\\Documents\\AI Frames\\TW2.jpg', folder)
    drive_service.upload_file('Test2IMG', 'C:\\Users\\HP\\Documents\\AI Frames\\TW3.jpg', folder)
    return folder


if __name__ == '__main__':
    main()

#detect_text('C:\\Users\\HP\\Documents\\AI Frames\\TW3.jpg')