import credentials
from apiclient.http import MediaFileUpload
from apiclient import errors
import urllib.request
import webbrowser
import requests
import os


#from google.appengine.api import users
#import webapp2

folderID = {}


def donate_id(id):

    post_data = {'id':id}
    r = requests.post("http://silencenamu.cafe24.com:9991/donations", post_data)
    #r = requests.post("http://jigsaw-puzzle.com:9991/donations", post_data)

    url = r.url

    # MacOS
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    # Windows
    # chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

    # Linux
    # chrome_path = '/uㄱㄱsr/bin/google-chrome %s'

    webbrowser.get(chrome_path).open_new(url)
    print ("[SYSTEM] Donate google account - %s" % id)


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
    #print(r.text)


def get_credentials_list():
    """
    global folderID
    credentials = []
    current_credential_list = []
    credentials_list = []
    credentials_dict = {}

    r = requests.get("http://1.234.65.53:9991/credentials")
    #r = requests.get("http://jigsaw-puzzle.com:9991/credentials")
    #print (r.text)

    list = r.text.split('\n')

    group = list[0][0]

    for idx in range(0, len(list)-1):

        if (idx % 2) == 0:
            strAccount = list[idx]
            indexOfUnder = strAccount.index('_')
            indexOfDot = strAccount.index('.')
            accountName = strAccount[indexOfUnder+1:indexOfDot]
            if (group == strAccount[0]):
                credentials_list.append(accountName)
                current_credential_list.append(accountName)
                credentials_dict[group] = credentials_list
            else:
                group = strAccount[0]
                credentials_list = []
                credentials_list.append(accountName)
                current_credential_list.append(accountName)
                credentials_dict[group] = credentials_list
            credentials.append(accountName)
        else:
            strJSON = list[idx]

            indexOfSF = strJSON.find("jigsaw_folder_id")
            strSF = strJSON[indexOfSF+20:]
            endOfSF = strSF.find('"')

            folderID[accountName] = strSF[:endOfSF]

            #dict = ast.literal_eval(strJSON)
            #print (dict)

    #credentials_list.pop()
    """


    credentials_dict = {}

    credentials_dict['a'] = ["silencenamu", "silencedeul", "silencesoop"]
    credentials_dict['b'] = ["silencebada", "silencettang", "silencemool"]
    credentials_dict['c'] = ["silencebyul", "silencebaram", "silencebool"]
    credentials_dict['d'] = ["silencepado", "somajigsaw1501"]

    current_credential_list = ["silencenamu", "silencedeul", "silencesoop", "silencebada", "silencettang", "silencemool", "silencebyul", "silencebaram", "silencebool", "silencepado", "somajigsaw1501"]

    print ("[SYSTEM] Get credentials group list from github :")
    print ("         {0}".format(credentials_dict))
    print ("[SYSTEM] Get credentials list from github :")
    print ("         {0}".format(current_credential_list))

    return credentials_dict, current_credential_list


"""
def get_current_credential_list():
    credentials_list = []
    #credentials_list = ["silencenamu", "silencedeul", "silencesoop", "silencebada", "silencettang", "silencemool", "silencebyul", "silencebaram", "silencebool"]


    r = requests.get("http://1.234.65.53:9991/credentials")
    list = r.text.split('\n')

    for idx in range(0, len(list)-1):

        if (idx % 2) == 0:
            strAccount = list[idx]
            indexOfUnder = strAccount.index('_')
            indexOfDot = strAccount.index('.')
            accountName = strAccount[indexOfUnder+1:indexOfDot]

            credentials_list.append(accountName)

    print ("[SYSTEM] Get credentials list from github :")
    print ("         {0}".format(credentials_list))

    return credentials_list
"""



def get_shared_folder_id(service, account):

    global folderID

    if account in folderID:
        print ("[SYSTEM] Success to get shared folder ID - '%s'" % account)
        return folderID[account]
    else:

        results = service.files().list(maxResults=40).execute()
        items = results.get('items', [])

        strFolderID = ""

        for item in items:
            emailAddress = item['owners'][0]['emailAddress']
            indexOfAt = emailAddress.index('@')
            accountName = emailAddress[:indexOfAt]

            if accountName == account:
                if item['title'] == 'jigsaw':
                    strFolderID = item['id']
                    print ("[SYSTEM] Success to get shared folder ID - '%s'" % account)
                    break
                """
                else:
                    #print ("[ERROR ] Fail to get shared folder ID - '%s'" % account)
                    #print ("         Create shared folder")
                    #folder = create_public_folder(account)
                    #strFolderID = folder['id']
                """

        folderID[account] = strFolderID

        return strFolderID


def print_files_in_shared_folder(account):

    service = credentials.get_service(account)
    results = service.files().list(maxResults=30).execute()
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



def upload_file(service, folderID, title, description, mime_type, filepath):
    #service = credentials.get_service(account)
    #folderID = get_shared_folder_id(service, account)
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
        }]
    }

    try:
        file = service.files().insert( body=body,media_body=media_body).execute()
        #print ("\n[UPLOAD] < {0} > on google drive - '{1}'".format(fileName, account))
        print ("\n[UPLOAD] < {0} > on google drive".format(fileName))
        return file

    except Exception as e:
        print ('[ERROR ] An error occurred: %s' % e)
        print ("         Failed upload file - '{0}'".format(filepath))
        return None



def delete_file(service, file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        print ("[DELETE] Deleted file - {0}".format(file_id))
    except errors.HttpError as error:
        print('[ERROR ] An error occurred: %s' % error)



def print_file_list_of_all_account():
    receivedCredential, accountList = get_credentials_list()
    for i in range(0, len(accountList)):
        print_files_in_shared_folder(accountList[i])



def delete_all_files_of_all_account():
    receivedCredential, accountList = get_credentials_list()

    for i in range(0, len(accountList)):
        service = credentials.get_service(accountList[i])
        items = get_file_id_in_shared_folder(service, accountList[i])
        for item in items:
            delete_file(service, item['id'])
        print("[DELETE] Deleted files in google drive - '%s'\n" % accountList[i])

    if os.path.isfile("metadata.json"):
        os.remove("metadata.json")
        print("[DELETE] Deleted metadata.json")
    else:
        print ("[ERROR ] Doesn't exist metadata.json")


def delete_all_files_of_one_account(account):
    service = credentials.get_service(account)
    items = get_file_id_in_shared_folder(service, account)
    for item in items:
        delete_file(service, item['id'])
    print("[DELETE] Deleted files in google drive - '%s'\n" % account)



def downlaod_file(id1, id2, id3, fileName):
    url = "https://drive.google.com/uc?export=download&id=" + id1

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        CHUNK = 16 * 1024
        downloadPath = os.getcwd() + "/cache/"
        with open(downloadPath + fileName, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)

        print ("[ DOWN ] Downloaded %s" % fileName)

    except Exception as e:

        url2 = "https://drive.google.com/uc?export=download&id=" + id2

        try:
            request = urllib.request.Request(url2)
            response = urllib.request.urlopen(request)

            CHUNK = 16 * 1024
            downloadPath = os.getcwd() + "/cache/"
            with open(downloadPath + fileName, 'wb') as f:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)

            print ("[ DOWN ] Downloaded %s" % fileName)

        except Exception as e:
            url3 = "https://drive.google.com/uc?export=download&id=" + id3

            try:
                request = urllib.request.Request(url3)
                response = urllib.request.urlopen(request)

                CHUNK = 16 * 1024
                downloadPath = os.getcwd() + "/cache/"
                with open(downloadPath + fileName, 'wb') as f:
                    while True:
                        chunk = response.read(CHUNK)
                        if not chunk:
                            break
                        f.write(chunk)

                print ("[ DOWN ] Downloaded %s" % fileName)

            except Exception as e:
                print ('[ERROR ] An error occurred: %s' % e)


def downlaod_one_file(id, fileName):
    url = "https://drive.google.com/uc?export=download&id=" + id

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        CHUNK = 16 * 1024
        downloadPath = os.getcwd() + "/cache/"
        with open(downloadPath + fileName, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)

        print ("[ DOWN ] Downloaded %s" % fileName)

    except Exception as e:
                print ('[ERROR ] An error occurred: %s' % e)


def print_files_in_account(account):

    service = credentials.get_service(account)
    results = service.files().list(maxResults=50).execute()
    items = results.get('items', [])
    cnt = 0

    print("\n[SYSTEM] Print all file list - '%s'" % account)
    print ("                File Name             (File ID)")
    print ('         ------------------------------------------------')
    if not items:
        print("[SYSTEM] ------------ Shared folder is empty ------------")
    else:
        for item in items:
            print ('         {0} ({1})'.format(item['title'], item['id']))
            cnt += 1
        if cnt == 0:
            print("[SYSTEM] ------------ Shared folder is empty ------------")
    print ('         ------------------------------------------------\n')
    return items


def print_all_file_list_of_all_account():
    receivedCredential, accountList = get_credentials_list()
    for i in range(0, len(accountList)):
        print_files_in_account(accountList[i])



# To delete all file in google drive -> Using children() method
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



def check_file_id(fileID):

    url = "https://drive.google.com/uc?export=view&id=" + fileID

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        return True

    except Exception as e:
        #print ('[ERROR ] An error occurred: %s' % e)
        return False






"""
# Using list() method
def get_file_id_in_shared_folder(service, account):

    results = service.files().list(maxResults=15).execute()
    items = results.get('items', [])
    folderID = get_shared_folder_id(service, account)
    cnt = 0
    idList = []

    if not items:
        print("[SYSTEM] ------------ Shared folder is empty ------------")
    else:
        for item in items:
            if len(item['parents']) != 0:
                if item['parents'][0]['id'] == folderID:
                    idList.append(item['id'])
                    cnt += 1
        if cnt == 0:
            print("[SYSTEM] ------------ Shared folder is empty ------------")
    return idList
"""



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