import httplib2
import os
from apiclient import discovery
from oauth2client import client, file, tools
import oauth2client

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES              = ['https://www.googleapis.com/auth/drive',
                       'https://www.googleapis.com/auth/drive.file',
                       'https://www.googleapis.com/auth/drive.appdata',
                       'https://www.googleapis.com/auth/drive.apps.readonly',
                       'https://www.googleapis.com/auth/drive.metadata.readonly'
                      ]
#CLIENT_SECRET_FILE  = 'client_secret.json'
APPLICATION_NAME    = 'GOOGLE DRIVE API TEST APP'



def get_service(account):
    credentials = get_credentials(account)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    return service

def get_credentials(account):
    home_dir = os.path.expanduser(os.getcwd() + "/credential")
    credential_dir = os.path.join(home_dir, account)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    fileName = 'google_oauth_credential.json'
    credential_path = os.path.join(credential_dir, fileName)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:

        flow = client.flow_from_clientsecrets("credential/" + account + "/client_secret.json", SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

