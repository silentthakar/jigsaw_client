import httplib2
from apiclient import discovery
import oauth2client
import requests
import googleDrive
import os
import sys

def get_service(account):
    credentials = get_credentials(account)
    #credentials.refresh(httplib2.Http())
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

    flag = 0
    r = requests.get("http://1.234.65.53:9991/credentials")
    jsonText = r.text

    list = r.text.split('\n')

    for idx in range(0, len(list)-1):

        if (idx % 2) == 0:
            strAccount = list[idx]
            indexOfUnder = strAccount.index('_')
            indexOfDot = strAccount.index('.')
            accountName = strAccount[indexOfUnder+1:indexOfDot]

            if accountName == account:
                credential_name = account + "_credential.json"
                strJSON = list[idx+1]

                indexOfSF = strJSON.find("jigsaw_folder_id")
                strSF = strJSON[indexOfSF+20:]
                endOfSF = strSF.find('"')

                frontJSON = strJSON[:indexOfSF-3]
                endJSON = strJSON[indexOfSF+endOfSF+21:]
                jsonText = frontJSON + endJSON
                break
            else:
                cnt += 1

    if cnt == (len(list)-1) / 2:
        print ("[ERROR ] Input the wrong account name")
        sys.exit(0)

    # Create credential.json
    f = open("./credential/"+credential_name, 'w')
    f.write(jsonText)
    f.close()

    credential_path = os.path.join(credential_dir, credential_name)

    # read credential to get store!
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    # Delete already read credential filer
    if os.path.isfile(credential_path):
        os.remove(credential_path)

    #googleDrive.revoke_credentials(account)

    if not credentials or credentials.invalid:
        print ("[ERROR ] That credential is wrong file, Please get credential again")
        googleDrive.donate_id(account)

    return credentials


def get_credentials_by_id(id):

    data = {'id':id}
    r = requests.post("http://silencenamu.cafe24.com:9991/credentials", params=data)
    print(r.text)