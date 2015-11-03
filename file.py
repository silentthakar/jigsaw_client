import googleDrive
import os
import json
import ast
import credentials
import zipfile
import sys
import threading
#from queue import Queue
#import time

infoList = []
finished_infoList = []
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
            account = ""
            for_download_str = ""
            dict = {}
            dict['fileName'] = 0
            readJSON.append(dict)

            fileName = readJSON[0]['fileName']

            while (len(readJSON) != 1):

                if readJSON[item]['fileName'] == fileName:
                    if readJSON[item]['indexOfChunk'] == idx:
                        lastIdx = readJSON[item]['numberOfChunks']

                        for key_account in readJSON[item]['origin']:
                            account = key_account
                            for_download_str = for_download_str + readJSON[item]['origin'][account] + '/'

                        for key_account in readJSON[item]['replication']:
                            account = key_account
                            for_download_str = for_download_str + readJSON[item]['replication'][account] + '/'

                        del readJSON[item]
                        idx += 1
                        item = 0

                        if idx == lastIdx:
                            for_download_str = fileName + '/' + for_download_str[:len(for_download_str)-1]
                            print ("         Uploaded FileName :  " + fileName)
                            print ("         Download  Strings :  " + for_download_str + '\n')
                            fileName = readJSON[item]['fileName']
                            for_download_str = ""
                            idx = 0
                    else:
                        item += 1
                        if item > len(readJSON)-1:
                            item = 0
        else:
            print("[SYSTEM] --------------- You didn't upload file on google drive ---------------")

    else:
        print("[ERROR ] Doesn't exist metadata.json")


def deleteFile(fileName):

    if os.path.isfile("metadata.json"):
        f = open("metadata.json", "r")
        readJSON = json.load(f)
        f.close()

        print ("[SYSTEM] Read metadata, Start remove chunk file")
        idx = 0
        item = 0

        while 1:
            if readJSON[item]['fileName'] == fileName:
                if readJSON[item]['indexOfChunk'] == idx:
                    lastIdx = readJSON[item]['numberOfChunks']

                    for key_account in readJSON[item]['origin']:
                        account = key_account
                        service = credentials.get_service(account)
                        googleDrive.delete_file(service, readJSON[item]['origin'][account])

                    for key_account in readJSON[item]['replication']:
                        account = key_account
                        service = credentials.get_service(account)
                        googleDrive.delete_file(service, readJSON[item]['replication'][account])

                    print("[DELETE] Removed chunk({0}) file - {1}\n".format(idx+1, readJSON[item]['chunkName']))
                    del readJSON[item]
                    idx += 1
                    item = 0
                    if idx == lastIdx:
                        print ("[DELETE] Deleted file on google drive - '%s'" % fileName)
                        break
                else:
                    item += 1
            else:
                item += 1

        if len(readJSON) == 0:
            os.remove("metadata.json")
            print ("[DELETE] Delete metadata.json")
        else:
            # Create metadata.json
            f = open('metadata.json', 'w')
            json.dump(readJSON, f, indent=4)
            f.close()
            print ("[SYSTEM] Remove metadata of '%s'" % fileName)

    else:
        print("[ERROR ] Doesn't exist metadata.json")


def zip_dir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def uploadFile(inputFile):

    #global infoList

    chunkInfoList, used_credential_list = splitFile(inputFile)

    division_thread_by_account(chunkInfoList, used_credential_list)

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

    createMetaData()

    division_thread_to_replicate(used_credential_list)

    createMetaDataForReplicate()


"""
# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        division_thread_by_account(item)
        q.task_done()
"""


def splitFile(inputFile):

    inputFilePath = os.path.abspath(inputFile)

    kilobytes = 1024
    Megabytes = kilobytes * 1024
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
        chunkInfoList = []
        used_credential = []
        circle = 0
        idx = 0

        # Received All Credential List
        credentials_list = googleDrive.get_current_credential_list()

        # Received All Credential Dictionary divided by group
        receivedCredential = googleDrive.get_credentials_list()


        uploadfilePath = os.getcwd() + "/cache"
        if not os.path.isdir(uploadfilePath):
            os.makedirs(uploadfilePath)
        uploadfilePath = uploadfilePath + '/'

        for i in range(0, bytes + 1, chunkSize):
            #fn1 = fileName + "%s" % i
            idx += 1
            fn1 = fileName + "%s" % idx
            f = open(uploadfilePath+fn1, 'wb')
            f.write(data[i: i + chunkSize])
            f.close()

            print ("[CREATE] Created chunk file({0}) - '{1}'".format(indexOfChunk+1, fn1))

            # Set to upload google drive account
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

            file_dict = {}
            key_account = credentials_list[credentialIndex]
            file_dict[key_account] = "null"
            dict['origin'] = file_dict
            #dict['account'] = credentials_list(credentialIndex)

            # Make account list for replication
            for group in receivedCredential:
                if credentials_list[credentialIndex] in receivedCredential[group]:
                    credentials_list_in_group = receivedCredential[group]
                    remove_used_credential_index = credentials_list_in_group.index(credentials_list[credentialIndex])
                    replica_list = credentials_list_in_group.copy()
                    replica_list.pop(remove_used_credential_index)

                    if len(replica_list) > 1:
                        break
                    elif len(replica_list) == 1:
                        replica_list.append(credentials_list[credentialIndex+1])
                        break
                    else:
                        replica_list.append(credentials_list[credentialIndex+1])
                        replica_list.append(credentials_list[credentialIndex+2])
                        break

            # Input account replication list
            replica_dict = {}
            if circle % 2 == 0:
                replica_dict[replica_list.pop()] = "null"
                replica_dict[replica_list.pop()] = "null"
                dict['replication'] = replica_dict
            else:
                replica_dict[replica_list.pop(0)] = "null"
                replica_dict[replica_list.pop(0)] = "null"
                dict['replication'] = replica_dict

            # Input used credential list
            for account in dict['origin']:
                if account not in used_credential:
                    used_credential.append(account)

            for account in dict['replication']:
                if account not in used_credential:
                    used_credential.append(account)

            # Input dictionary in List
            chunkInfoList.append(dict)
            indexOfChunk += 1

        # Input used credential list to send divide thread module
        #chunkInfoList.append(used_credential)
        print ("[SYSTEM] Finish split file - Created chunk file '{0}'\n".format(indexOfChunk))

        return chunkInfoList, used_credential

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
            sys.exit(0)


def division_thread_by_account(chunkInfoList, used_credential_list):

    """
    # Received Credential Array
    receivedCredential =  googleDrive.get_credentials_list()

    for group in receivedCredential:
        #if len(receivedCredential[group]) == 3:
        if group == 'a':
            credentials_list = receivedCredential[group]
    """
    # To get used credential list
    credentials_list = used_credential_list.copy()

    noOfThread = len(credentials_list)

    for i in range(noOfThread):
        account = credentials_list.pop()
        accountSortList = sort_list_by_account(chunkInfoList, account)
        th = threading.Thread(target=uploadGoogledrive, args=(accountSortList, account, "origin", ))
        th.setDaemon(True)
        th.start()
        print ("\n[SYSTEM] ============================= Uploading Thread Start - {0} ============================\n".format(i+1))

    main_thread = threading.current_thread()

    for th in threading.enumerate():
        if th is main_thread:
            continue
        th.join()
        print ("\n[SYSTEM] ===================================== Thread End ======================================\n")




def sort_list_by_account(infoList, account):

    #global infoList

    accountInfoList = []
    user_id = account

    for item in range(0, len(infoList)):
        for account in infoList[item]['origin']:
            if account == user_id:
                accountInfoList.append(infoList[item])
    print ("[SYSTEM] Sort chunk file list by '{0}'".format(account))

    return accountInfoList



def division_thread_to_replicate(used_credential_list):

    global infoList

    # To get used credential list
    credentials_list = used_credential_list.copy()

    noOfThread = len(credentials_list)

    for i in range(noOfThread):
        account = credentials_list.pop()
        accountSortList = sort_list_by_replication_account(infoList, account)
        th = threading.Thread(target=uploadGoogledrive, args=(accountSortList, account, "replication", ))
        th.setDaemon(True)
        th.start()
        print ("\n[SYSTEM] ======================= Uploading replication Thread Start - {0} ======================\n".format(i+1))

    main_thread = threading.current_thread()

    for th in threading.enumerate():
        if th is main_thread:
            continue
        th.join()
        print ("\n[SYSTEM] ===================================== Thread End ======================================\n")



def sort_list_by_replication_account(readJSON, account):

    accountInfoList = []
    user_id = account

    for item in range(0, len(infoList)):
        for account in readJSON[item]['replication']:
            if account == user_id:
                accountInfoList.append(readJSON[item])
    print ("[SYSTEM] Sort chunk file list by '{0}'".format(account))

    return accountInfoList



def uploadGoogledrive(accountSortList, account, flag):

    uploadfilePath = os.getcwd() + "/cache/"
    service = credentials.get_service(account)
    folderID = googleDrive.get_shared_folder_id(service, account)

    for i in range(0, len(accountSortList)):
        fn1 = accountSortList[i]['chunkName']

        # upload_file(업로드된후 파일명, 파일설명, 파일타입, 실제 올릴 파일경로)
        uploadFile = googleDrive.upload_file(service, folderID, "%s" % fn1, '', '', uploadfilePath + fn1)

        if type(uploadFile) == 'NoneType':
             print ("[ERROR ] Failed upload Chunk({0})- '{1}'".format(accountSortList[i]['indexOfChunk']+1, fn1))

        else:
            if flag == "origin":
                global infoList

                if accountSortList[i]['origin'][account] == "null":
                    accountSortList[i]['origin'][account] = uploadFile['id']
                    infoList.append(accountSortList[i])

                    print ("[SYSTEM] Stored metadata of original Chunk({0})- '{1}'".format(accountSortList[i]['indexOfChunk']+1, fn1))

            elif flag == "replication":
                global finished_infoList

                if accountSortList[i]['replication'][account] == "null":
                    accountSortList[i]['replication'][account] = uploadFile['id']

                    # Delete already uploaded chunk file
                    for key in accountSortList[i]['replication']:
                        if key != account:
                            if accountSortList[i]['replication'][key] != "null":
                                if fn1 == uploadFile['title']:
                                    finished_infoList.append(accountSortList[i])
                                    print ("[SYSTEM] Stored metadata of replication of Chunk({0})- '{1}'".format(accountSortList[i]['indexOfChunk']+1, fn1))
                                    if os.path.isfile(uploadfilePath+fn1):
                                        os.remove(uploadfilePath+fn1)
                                        print ("[DELETE] Remove already uploaded chunk file - '{0}'".format(fn1))

            else:
                print ("[ERROR ] Failed upload Chunk({0})- '{1}'".format(accountSortList[i]['indexOfChunk']+1, fn1))


    #return infoList


def createMetaData():

    global infoList

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
    print ("\n-----------------------------------------------------------------------------------------------------------------")
    print ("|                                        Finished Upload original file                                            |")
    print ("-----------------------------------------------------------------------------------------------------------------\n\n")



def createMetaDataForReplicate():

    global finished_infoList

    # already exist metadata.json
    if os.path.isfile("metadata.json"):
        with open("metadata.json") as f:
            data = json.load(f)

        lenOfinfolist = len(finished_infoList)
        lenOfData = len(data)

        if lenOfinfolist == lenOfData:
            serialized_dict = json.dumps(finished_infoList)
        else:
            data = data[:lenOfData-lenOfinfolist]
            data = data + finished_infoList
            serialized_dict = json.dumps(data)

        dictJSON = ast.literal_eval(serialized_dict)
        f.close()

        # Create metadata.json
        f = open('metadata.json', 'w')
        json.dump(dictJSON, f, indent=4)
        f.close()

        print ("\n[CREATE] Created metadata of '%s'" % infoList[0]['fileName'])

    else:
        print ("[ERROR ] Doesn't exist metadata file")




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
    fileIdList = fileIdList[1:]

    noOfThread = 10
    start = 0
    totalCount = int(len(fileIdList) / 3)
    noOfChunks = totalCount

    originIdList = []
    replicaOneList = []
    replicaTwoList = []

    copyOfList = fileIdList.copy()
    for item in range (0, totalCount):
        originIdList.append(copyOfList.pop(0))
        replicaOneList.append(copyOfList.pop(0))
        replicaTwoList.append(copyOfList.pop(0))

    if totalCount < 10:
        idx = 0
        copyOfOriginIdList = originIdList.copy()
        copyOfRplicaOneList = replicaOneList.copy()
        copyOfRplicaTwoList = replicaTwoList.copy()
        for i in range(totalCount):
            th = threading.Thread(target=division_thread_by_one_item, args=(copyOfOriginIdList.pop(0), copyOfRplicaOneList.pop(0), copyOfRplicaTwoList.pop(0), idx, ))
            th.setDaemon(True)
            th.start()
            print ("\n[SYSTEM] ============================ Downloading Thread Start - {0} ===========================\n".format(i+1))
            idx += 1
    else:
        dividedCount = int(totalCount / noOfThread)
        while (dividedCount < 2):
            noOfThread -= 1
            dividedCount = int(totalCount / noOfThread)
        remainCount = totalCount % noOfThread
        addThread = int(remainCount / dividedCount)
        lastRemain = remainCount % dividedCount

        for i in range(noOfThread + addThread):
            if start > (noOfThread*dividedCount + (addThread*dividedCount)):
                slicedOriginIdList = originIdList[start:start+lastRemain]
                slicedReplicaOneList = replicaOneList[start:start+lastRemain]
                slicedReplicaTwoList = replicaTwoList[start:start+lastRemain]
            else:
                slicedOriginIdList = originIdList[start:start+dividedCount]
                slicedReplicaOneList = replicaOneList[start:start+dividedCount]
                slicedReplicaTwoList = replicaTwoList[start:start+dividedCount]
            th = threading.Thread(target=division_thread_by_download_count, args=(slicedOriginIdList, slicedReplicaOneList, slicedReplicaTwoList, start, ))
            th.setDaemon(True)
            th.start()
            print ("\n[SYSTEM] ============================ Downloading Thread Start - {0} ===========================\n".format(i+1))
            start += dividedCount

    main_thread = threading.current_thread()

    for th in threading.enumerate():
        if th is main_thread:
            continue
        th.join()
        print ("\n[SYSTEM] ===================================== Thread End ======================================\n")


    print("[SYSTEM] Downloaded all chunk file for download\n")

    joinFiles(fileName, noOfChunks)


def division_thread_by_download_count(originIdList, replicaOneList, replicaTwoList, start):
    for item in range(len(originIdList)):
        googleDrive.downlaod_file(originIdList[item], replicaOneList[item], replicaTwoList[item], "chunk{0}".format(start+item))


def division_thread_by_one_item(originID, replica1ID, replica2ID, idx):
        googleDrive.downlaod_file(originID, replica1ID, replica2ID, "chunk{0}".format(idx))



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


