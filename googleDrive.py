import credentials
from apiclient.http import MediaFileUpload
from apiclient import errors
import urllib.request
import webbrowser
import requests
import os
import time

folderID = {}


def donate_id(id):

    global folderID

    post_data = {'id':id}
    r = requests.post("http://silencenamu.cafe24.com:9991/donations", post_data)
    #r = requests.post("http://jigsaw-puzzle.com:9991/donations", post_data)

    url = r.url

    # MacOS
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    # Windows
    # chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

    # Linux
    # chrome_path = '/usr/bin/google-chrome %s'

    webbrowser.get(chrome_path).open(url)
    print ("[SYSTEM] Donate google account - %s" % id)

    """
    time.sleep(5)
    while (id in current_list):
        current_list = get_credentials_list()

    folder = create_public_folder(id)
    folderID[id] = folder['id']
    """



def create_public_folder(account):

    service = credentials.get_service(account)

    body = {
    'title': "jigsaw",
    'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().insert(body=body).execute()

    permission = {
    'value': '',
    'type': 'anyone',
    'role': 'reader'
    } # https://developers.google.com/drive/web/manage-sharing

    service.permissions().insert(fileId=folder['id'], body=permission).execute()
    print ("[CREATE] Create shared folder in google drive")

    return folder


def revoke_credentials(id):

    data = {'id':id}
    r = requests.delete("http://silencenamu.cafe24.com:9991/credentials", params=data)
    #r = requests.delete("http://jigsaw-puzzle.com:9991/credentials", params=data)
    print(r.text)


def get_credentials_list():

    r = requests.get("http://1.234.65.53:9991/credentials")
    #r = requests.get("http://jigsaw-puzzle.com:9991/credentials")

    #print (r.text)
    credentials_list = r.text.split("_credential.json\n")
    #print(credentials_list)
    credentials_list.pop()

    return credentials_list



def print_files_in_shared_folder(account):

    service = credentials.get_service(account)
    results = service.files().list(maxResults=20).execute()
    items = results.get('items', [])
    folderID = get_shared_folder_id(service, account)
    cnt = 0

    print("\n[SYSTEM] Print file list - '%s'" % account)
    print ("                File Name             (File ID)")
    print ('         ------------------------------------------------')
    if not items:
        print("[SYSTEM] ------------ Shared folder is empty ------------")
    else:
        for item in items:
            if len(item['parents']) != 0:
                if item['parents'][0]['id'] == folderID:
                    print ('         {0} ({1})'.format(item['title'], item['id']))
                    cnt += 1
        if cnt == 0:
            print("[SYSTEM] ------------ Shared folder is empty ------------")
    print ('         ------------------------------------------------\n')
    return items

"""
def print_files_in_shared_folder_older_version(account):
    service = credentials.get_service(account)
    folderID = get_shared_folder_id(service, account)

    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token

            children = service.children().list(folderId=folderID, **param).execute()

            print ("\n[SYSTEM] Print file list - '%s'" % account)
            print ("                File Name             (File ID)")
            print ('         ------------------------------------------------')
            for child in children.get('items', []):
                file_id = child['id']
                try:
                    file = service.files().get(fileId=file_id).execute()
                    print ('         {0} ({1})'.format(file['title'], file_id))
                    #print ('File Id: %s' % child['id'])
                except errors.HttpError as error:
                    print ('[ERROR ] An error occurred: %s' % error)

            if len(children['items']) == 0:
                print("[SYSTEM] ------------ Shared folder is empty ------------")
            print ('         ------------------------------------------------\n')

            page_token = children.get('nextPageToken')
            if not page_token:
                break

        except errors.HttpError as error:
            print ('[ERROR ] An error occurred: %s' % error)
            return None
            break

"""

# To delete all file in google drive
def get_file_id_in_shared_folder(service, account):
    #service = credentials.get_service(account)
    folderID = get_shared_folder_id(service, account)

    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token

            children = service.children().list(folderId=folderID, **param).execute()
            items = children.get('items', [])

            page_token = children.get('nextPageToken')
            if not page_token:
                return items
                break


        except errors.HttpError as error:
            print ('[ERROR ] An error occurred: %s' % error)
            return None
            break



def upload_file(account, title, description, mime_type, filepath):
    service = credentials.get_service(account)
    folderID = get_shared_folder_id(service, account)
    fileIndexOfSlash = filepath.rfind('/')
    fileName = filepath[fileIndexOfSlash+1:]

    media_body = MediaFileUpload(filepath, mimetype=mime_type, resumable=True)
    body = {
        'title': title,
        'description': description,
        'mimeType': mime_type,
        "parents": [{
            "kind": "drive#fileLink",
            "id": folderID,        # <<<!!!!이 부분은 public으로 설정한 폴더의 ID를 써줘야한다!!!!>>>
            # https://drive.google.com/folderview?id=0B-_r0Nosw-jtVXFGN2pjMnFKV2s&usp=sharing -> silencethakar
            # https://drive.google.com/folderview?id=0B5iptnvBTi5SQ3hoNUx1ZlU2MDQ&usp=sharing -> silencenamu
            # https://drive.google.com/folderview?id=0B-oP1y2aj8zbUGNjMkhUNGs3OGM&usp=sharing -> silencedeul
            # https://drive.google.com/folderview?id=0B6YNyAA5dnxEMGFvdlE2ekQzR3M&usp=sharing -> silencesoop
        }]
    }

    try:
        file = service.files().insert( body=body,media_body=media_body).execute()
        print ("\n[UPLOAD] < {0} > on google drive - '{1}'".format(fileName, account))
        return file

    except Exception as e:
        print("[ERROR ] %s" % e)
        return None


def get_shared_folder_id(service, account):

    global folderID

    if account in folderID:
        return folderID[account]
    else:

        results = service.files().list(maxResults=100).execute()
        items = results.get('items', [])

        folderID = ""

        for item in items:
            emailAddress = item['owners'][0]['emailAddress']
            indexOfAt = emailAddress.index('@')
            accountName = emailAddress[:indexOfAt]

            if accountName == account:
                if item['title'] == 'jigsaw':
                    folderID = item['id']
                    print ("[SYSTEM] Success to get shared folder ID - '%s'" % account)
                    break

        return folderID


def delete_file(service, file_id):

    try:
        service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        print('[ERROR ] An error occurred: %s' % error)

"""
def delete_all_files(account, max=10):

    service = credentials.get_service(account)
    results = service.files().list(maxResults=max).execute()
    items = results.get('items', [])

    if not items:
        print('[ERROR ] No files found.')
    else:
        for item in items:
            try:
                service.files().delete(fileId=item['id']).execute()
                print("[DELETE] Deleted all of file in google drive - '%s'" % account)
            except errors.HttpError as error:
                print('[ERROR ] An error occurred: %s' % error)
"""

def read_file_list_of_all_account(accountList):
    for i in range(0, len(accountList)):
        print_files_in_shared_folder(accountList[i])


def delete_all_files_of_all_account():
    accountList = get_credentials_list()
    for i in range(0, len(accountList)):
        service = credentials.get_service(accountList[i])
        items = get_file_id_in_shared_folder(service, accountList[i])
        for item in items:
            delete_file(service, item['id'])
        print("[DELETE] Deleted files in google drive - '%s'\n" % accountList[i])
    os.remove("metadata.json")
    print("[DELETE] Deleted metadata.json")



def delete_all_files_of_one_account(account):
    service = credentials.get_service(account)
    items = get_file_id_in_shared_folder(service, account)
    for item in items:
        delete_file(service, item['id'])
    print("[DELETE] Deleted files in google drive - '%s'\n" % account)
    print("")


def downlaod_file(id, fileName):
    url = "https://drive.google.com/uc?export=download&id=" + id

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    CHUNK = 16 * 1024
    with open('./cache/'+ fileName, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
    print ("[ DOWN ] Downloaded %s" % fileName)