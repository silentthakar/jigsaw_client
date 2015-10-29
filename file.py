import googleDrive
import os
import json
import ast
import credentials
import zipfile
import sys
#import threading
#from queue import Queue
#import time
from threading import Thread

infoList = []
#lock = threading.Lock()
#q = Queue()

def printFileList():

    if os.path.isfile("metadata.json"):
        f = open("metadata.json", "r")
        readJSON = json.load(f)
        f.close()

        print("[SYSTEM] Print file list")
        if (len(readJSON) != 0):

            idx = 0
            item = 0
            for_download_str = ""
            dict = {}
            dict['fileName'] = 0
            readJSON.append(dict)

            fileName = readJSON[0]['fileName']

            while (len(readJSON) != 1):

                if readJSON[item]['fileName'] == fileName:
                    if readJSON[item]['indexOfChunk'] == idx:
                        lastIdx = readJSON[item]['numberOfChunks']
                        for_download_str = for_download_str + readJSON[item]['fileID'] + '/'
                        del readJSON[item]
                        idx += 1
                        if idx == lastIdx:
                            for_download_str = fileName + '/' + for_download_str[:len(for_download_str)-1]
                            print ("         Uploaded FileName :  " + fileName)
                            print ("         Download  Strings :  " + for_download_str + '\n')
                            fileName = readJSON[item]['fileName']
                            for_download_str = ""
                            idx = 0
        else:
            print("[SYSTEM] --------------- You didn't upload file on google drive ---------------")

    else:
        print("[ERROR ] Doesn't exist metadata.json")


def deleteFile(fileName):

    if os.path.isfile("metadata.json"):
        f = open("metadata.json", "r")
        readJSON = json.load(f)
        f.close()

        print ("[SYSTEM] Start remove chunk file")
        idx = 0
        item = 0

        """
        for item in range(0, len(readJSON)):
            if readJSON[item]['fileName'] == fileName:
                if readJSON[item]['indexOfChunk'] == idx:
                    service = credentials.get_service(readJSON[item]['account'])
                    googleDrive.delete_file(service, readJSON[item]['fileID'])
                idx += 1
            else:
                infoList.insert(0, readJSON[item])
        """

        for i in range(0, len(readJSON)):
            if readJSON[item]['fileName'] == fileName:
                if readJSON[item]['indexOfChunk'] == idx:
                    lastIdx = readJSON[item]['numberOfChunks']
                    service = credentials.get_service(readJSON[item]['account'])
                    googleDrive.delete_file(service, readJSON[item]['fileID'])
                    print("[DELETE] Removed chunk file - {0}".format(readJSON[item]['chunkName']))
                    del readJSON[item]
                    idx += 1
                    if idx == lastIdx:
                        if len(readJSON) == 0:
                            os.remove("metadata.json")
                        break
            else:
                item += 1


        print ("[DELETE] Deleted file on google drive - '%s'" % fileName)

        # Create metadata.json
        f = open('metadata.json', 'w')
        json.dump(readJSON, f, indent=4)
        f.close()

        print ("[DELETE] Remove metadata of '%s'" % fileName)

    else:
        print("[ERROR ] Doesn't exist metadata.json")


def zip_dir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def uploadFile(inputFile):

    #global infoList

    infoList = splitFile(inputFile)

    division_thread_by_account(infoList)

    """
    # Create the queue and thread pool.
    for i in range(3):
        t = threading.Thread(target=worker)
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t.start()

    # stuff work items on the queue (in this case, just a number).
    start = time.perf_counter()
    for item in range(5):
        q.put(item)

    q.join()       # block until all tasks are done
    """

    print (infoList)

    #infoList = uploadGoogledrive(infoList)

    #createMetaData(infoList)



def division_thread_by_account(infoList):

    # Received Credential Array
    receivedCredential =  googleDrive.get_credentials_list()

    for group in receivedCredential:
        #if len(receivedCredential[group]) == 3:
        if group == 'a':
            credentials_list = receivedCredential[group]

    accountSortList = sort_list_by_account(credentials_list.pop(), infoList)
    th1 = Thread(target=uploadGoogledrive, args=(accountSortList,))
    accountSortList = sort_list_by_account(credentials_list.pop(), infoList)
    th2 = Thread(target=uploadGoogledrive, args=(accountSortList,))
    accountSortList = sort_list_by_account(credentials_list.pop(), infoList)
    th3 = Thread(target=uploadGoogledrive, args=(accountSortList,))
    th1.start()
    th1.join()
    print ("[SYSTEM] Thread - 1 Start")
    th2.start()
    th2.join()
    print ("[SYSTEM] Thread - 2 Start")
    th3.start()
    th3.join()
    print ("[SYSTEM] Thread - 3 Start")

"""
# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        division_thread_by_account(item)
        q.task_done()
"""


def splitFile(inputFile):

    #global infoList

    inputFilePath = os.path.abspath(inputFile)

    kilobytes = 1024
    Megabytes = kilobytes * 1000
    chunkSize = int(Megabytes * 8)

    indexOfPoint = inputFilePath.rfind('.')
    indexOfSlash = inputFilePath.rfind('/')
    fileName = inputFilePath[indexOfSlash+1:indexOfPoint]

    # read input file
    if os.path.isfile(inputFilePath):
        f = open(inputFilePath, 'rb')
        data = f.read()
        f.close()
        print ("\n[SYSTEM] Finished read binary file for upload")

        # get the length of data, ie size of the input file in bytes
        bytes = len(data)

        # Calculate the number of chunks to be created
        if bytes < chunkSize:
            chunkSize = int(kilobytes * 512)
            noOfChunks = bytes / chunkSize
            if (bytes % chunkSize):
                noOfChunks += 1
        else:
            noOfChunks = bytes / chunkSize
            if (bytes % chunkSize):
                noOfChunks += 1

            else:
                while (noOfChunks > 41):
                    chunkSize *= 2
                    noOfChunks = bytes / chunkSize
                    if (bytes % chunkSize):
                        noOfChunks += 1


        # Initialize JSON text variable
        indexOfChunk = 0
        infoList = []

        # Received Credential Array
        receivedCredential =  googleDrive.get_credentials_list()

        for group in receivedCredential:
            #if len(receivedCredential[group]) == 3:
            if group == 'a':
                credentials_list = receivedCredential[group]


        chunkNames = []
        circle = 0

        uploadfilePath = os.getcwd() + "/cache"
        if not os.path.isdir(uploadfilePath):
            os.makedirs(uploadfilePath)
        uploadfilePath = uploadfilePath + '/'

        for i in range(0, bytes + 1, chunkSize):
            fn1 = fileName + "%s" % i
            chunkNames.append(fn1)
            f = open(uploadfilePath+fn1, 'wb')
            f.write(data[i: i + chunkSize])
            f.close()

            print ("[CREATE] Created chunk file({0}) - '{1}'".format(indexOfChunk+1, fn1))


            if indexOfChunk < len(credentials_list):
                credentialIndex = indexOfChunk
            else:
                credentialIndex = indexOfChunk % len(credentials_list)
                circle += 1

            # Input metadata of chunk file in dictionary
            dict = {}
            dict['fileName'] = inputFilePath[indexOfSlash+1:]
            dict['numberOfChunks'] = int(noOfChunks)
            dict['indexOfChunk'] = indexOfChunk
            dict['chunkName'] = fn1

            replicaList = credentials_list.copy()
            dict['account'] = replicaList.pop(credentialIndex)
            if circle % 2 == 0:
                dict['replication1'] = replicaList.pop()
                dict['replication2'] = replicaList.pop()
            else:
                dict['replication2'] = replicaList.pop()
                dict['replication1'] = replicaList.pop()


            # Input dictionary in List
            infoList.insert(indexOfChunk, dict)
            indexOfChunk += 1

        print ("[SYSTEM] Finish split file - Created chunk file '{0}'\n".format(indexOfChunk))

        return infoList

    else:
        if os.path.isdir(inputFilePath):
            print ("\n[SYSTEM] Input File is directory, Please make zip")
            zip = zipfile.ZipFile(fileName+".zip", 'w')
            zip_dir("./"+inputFilePath[indexOfSlash+1:], zip)
            zip.close()

            print ("\n[CREATE] Create a zip archive of a directory")
            uploadFile(fileName+".zip")
            sys.exit(0)
        else:
            print ("\n[ERROR ] Input the wrong file path")


def sort_list_by_account(account, infoList):

    #global infoList

    accountInfoList = []
    user_id = account

    for item in range(0, len(infoList)):
        if infoList[item]['account'] == user_id:
            accountInfoList.append(infoList[item])

    return accountInfoList



def uploadGoogledrive(accountSortList):

    global infoList

    uploadfilePath = os.getcwd() + "/cache/"
    account = accountSortList[0]['account']
    service = credentials.get_service(account)
    folderID = googleDrive.get_shared_folder_id(service, account)

    for i in range(0, len(accountSortList)):
        #with lock:
        fn1 = accountSortList[i]['chunkName']

        # upload_file(업로드된후 파일명, 파일설명, 파일타입, 실제 올릴 파일경로)
        uploadFile = googleDrive.upload_file(service, folderID, "%s" % fn1, '', '', uploadfilePath + fn1)

        accountSortList[i]['fileID'] = uploadFile['id']
        infoList.append(accountSortList[i])

        print ("[SYSTEM] Stored metadata of Chunk({0})- '{1}'".format(i+1, fn1))

        """
        # Delete already uploaded chunk file
        if fn1 == uploadFile['title']:
            if os.path.isfile(uploadfilePath+fn1):
                os.remove(uploadfilePath+fn1)
                print ("[DELETE] Remove already uploaded chunk file - '{0}'".format(fn1))
        """

    #return infoList


def createMetaData(infoList):

    # already exist metadata.json
    if os.path.isfile("metadata.json"):
        with open("metadata.json") as f:
            data = json.load(f)

        data = data + infoList
        serialized_dict = json.dumps(data)
        dictJSON = ast.literal_eval(serialized_dict)
        f.close()

    # write metadata.json
    else:
        # Convert list to dictionary
        serialized_dict = json.dumps(infoList)
        dictJSON = ast.literal_eval(serialized_dict)

    # Create metadata.json
    f = open('metadata.json', 'w')
    json.dump(dictJSON, f, indent=4)
    f.close()

    print ("\n[CREATE] Created metadata of '%s'" % infoList[0]['fileName'])



def downloadFile(downFile):

    f = open("metadata.json", "r")
    readJSON = json.load(f)
    f.close()

    noOfChunks = 0
    idx = 0
    cnt = 0

    print ("\n[SYSTEM] Finished read metadata for download\n")

    for item in range(0, len(readJSON)):
        if readJSON[item]['fileName'] == downFile:
            noOfChunks = readJSON[item]['numberOfChunks']
            googleDrive.downlaod_file(readJSON[item]['fileID'], "chunk%d" % idx)
            idx += 1
        else:
           cnt += 1
    if cnt == len(readJSON):
        print ("[ERROR ] That file doesn't exist in google drive")
    else:
        print("[SYSTEM] Downloaded all chunk filer for download\n")
        joinFiles(downFile, noOfChunks)


def downloadFileByString(download_string):

    fileIdList = download_string.split('/')
    fileName = fileIdList[0]
    noOfChunks = len(fileIdList)-1
    fileIdList = fileIdList[1:]
    idx = 0

    for idx in range(0, noOfChunks):
        googleDrive.downlaod_file(fileIdList[idx], "chunk%d" % idx)

    print("[SYSTEM] Downloaded all chunk file for download\n")
    joinFiles(fileName, noOfChunks)

def joinFiles(downFile, noOfChunks):

    dataList = []
    count = 0

    for i in range(0, noOfChunks, 1):
        f = open("./cache/chunk%d" % count, 'rb')
        dataList.append(f.read())
        print ("[ JOIN ] Read chunk%d" % count)
        f.close()
        os.remove("./Cache/chunk%d" % count)
        print ("[DELETE] Remove already joined chunk file - 'chunk{0}'".format(count))
        count += 1

    f = open("new%s" % downFile, 'wb')
    for data in dataList:
        f.write(data)
    f.close()
    print ("\n[SYSTEM] Finish join chunk files - Created '%s'\n" % downFile)


