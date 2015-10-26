import googleDrive
import os
import json
import ast
import credentials
from threading import Thread


def printFileList():

    if os.path.isfile("metadata.json"):
        f = open("metadata.json", "r")
        readJSON = json.load(f)
        f.close()

        idx = 0
        for_download_str = ""

        print("[SYSTEM] Print file list")

        for item in range(0, len(readJSON)):
            fileName = readJSON[item]['fileName']

            if readJSON[item]['fileName'] == fileName:
                if readJSON[item]['indexOfChunk'] == idx:
                    for_download_str = for_download_str + readJSON[item]['fileID'] + '/'
                idx += 1
            else:
                fileName = readJSON[item]['fileName']
                idx = 0

        for_download_str = fileName + '/' + for_download_str[:len(for_download_str)-1]
        print ("         Uploaded FileName :  " + fileName)
        print ("         Download  Strings :  " + for_download_str + '\n')
    else:
        print("[ERROR ] Doesn't exist metadata.json")


def deleteFile(fileName):
    f = open("metadata.json", "r")
    readJSON = json.load(f)
    f.close()

    infoList = []
    indexOfList = 0
    idx = 0
    for_download_str = ""

    print("[SYSTEM] Print file list")

    for item in range(0, len(readJSON)):
        if readJSON[item]['fileName'] == fileName:
            if readJSON[item]['indexOfChunk'] == idx:
                service = credentials.get_service(readJSON[item]['account'])
                googleDrive.delete_file(service, readJSON[item]['fileID'])
            idx += 1
        else:
            infoList.insert(indexOfList, readJSON[item])

    print ("[DELETE] Deleted file on google drive - '%s'" % fileName)

    # Convert list to dictionary
    serialized_dict = json.dumps(infoList)
    dictJSON = ast.literal_eval(serialized_dict)

    # Create metadata.json
    f = open('metadata.json', 'w')
    json.dump(dictJSON, f, indent=4)
    f.close()

    print ("[DELETE] Remove metadata of '%s'" % fileName)


def uploadFile(inputFile):

    infoList = splitFile(inputFile)

    infoList = uploadGoogledrive(infoList)

    createMetaData(infoList)


def splitFile(inputFile):

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
            noOfChunks = 4
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
        #receivedCredential =  googleDrive.get_credentials_list()
        receivedCredential = ["silencedeul", "silencesoop"]

        chunkNames = []

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

            if indexOfChunk < len(receivedCredential):
                credentialIndex = indexOfChunk
            else:
                credentialIndex = indexOfChunk % len(receivedCredential)

            # Input metadata of chunk file in dictionary
            dict = {}
            dict['fileName'] = inputFilePath[indexOfSlash+1:]
            dict['numberOfChunks'] = int(noOfChunks)
            dict['indexOfChunk'] = indexOfChunk
            dict['chunkName'] = fn1
            dict['account'] = receivedCredential[credentialIndex]

            # Input dictionary in List
            infoList.insert(indexOfChunk, dict)
            indexOfChunk += 1

        print ("[SYSTEM] Finish split file - Created chunk file '{0}'\n".format(indexOfChunk))

        return infoList

    else:
        print ("\n[ERROR ] Input the wrong file path")


def uploadGoogledrive(infoList):

    uploadfilePath = os.getcwd() + "/cache/"

    for i in range(0, len(infoList)):
        fn1 = infoList[i]['chunkName']

        # upload_file(업로드된후 파일명, 파일설명, 파일타입, 실제 올릴 파일경로)
        uploadFile = googleDrive.upload_file(infoList[i]['account'], "%s" % fn1, '', '', uploadfilePath + fn1)

        infoList[i]['fileID'] = uploadFile['id']

        print ("[SYSTEM] Stored metadata of Chunk({0})- '{1}'".format(i+1, fn1))


        # Delete already uploaded chunk file
        if fn1 == uploadFile['title']:
            if os.path.isfile(uploadfilePath+fn1):
                os.remove(uploadfilePath+fn1)
                print ("[DELETE] Remove already uploaded chunk file - '{0}'\n".format(fn1))


    return infoList


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
        print("[SYSTEM] Downloaded all chunk file for download\n")
        joinFiles(downFile, noOfChunks)


def downloadFileByString(download_string):

    fileIdList = download_string.split('/')
    fileName = fileIdList[0]
    noOfChunks = len(fileIdList)-1
    fileIdList = fileIdList[1:]
    idx = 0

    for item in fileIdList:
        googleDrive.downlaod_file(fileIdList[idx], "chunk%d" % idx)
        idx += 1

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


