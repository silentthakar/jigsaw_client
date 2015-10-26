import httplib2
from apiclient import discovery
import oauth2client
import requests
import googleDrive
import os
import sys

def get_service(account):
    credentials = get_credentials(account)
    print ("[SYSTEM] Get a crendetial - %s" % account)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    print ("[SYSTEM] Get a Service object - %s" % account)
    return service



def get_credentials(account):
    # Set path to write credential json
    credential_dir = os.path.expanduser(os.getcwd() + "/credential")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    cnt = 0
    credentials_list = googleDrive.get_credentials_list()

    for credential in credentials_list:
        if credential == account:
            credential_name = credential + "_credential.json"
            break
        else:
            cnt += 1

    if cnt == len(credentials_list):
        print ("[ERROR ] Input the wrong account name")
        sys.exit(0)
    else:

        url = "https://raw.githubusercontent.com/seoyujin/yujin_project/master/credentials/" + credential_name
        r = requests.get(url)
        jsonText = r.text

        # Create credential.json
        f = open("./credential/"+credential_name, 'w')
        f.write(jsonText)
        f.close()

        credential_path = os.path.join(credential_dir, credential_name)

        # read credential to get store!
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        # Delete already read credential file
        if os.path.isfile(credential_path):
            os.remove(credential_path)

        #googleDrive.revoke_credentials(account)

        if not credentials or credentials.invalid:
            print ("[ERROR ] That credential is wrong file, Please get credential again")
            googleDrive.donate_id(account)
            get_credentials(account)

        return credentials
