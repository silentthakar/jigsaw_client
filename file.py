import googleDrive
import os
import json
import ast


def uploadFile(inputFile):

    infoList = splitFile(inputFile)

    infoList = uploadGoogledrive(infoList)

    createMetaData(infoList)


def splitFile(inputFile):
    kilobytes = 1024
    someMegabytes = kilobytes * 512
    chunkSize = int(someMegabytes)

    indexOfPoint = inputFile.index('.')
    fileName = inputFile[:indexOfPoint]

    # read input file
    f = open(inputFile, 'rb')
    data = f.read()
    f.close()

    # get the length of data, ie size of the input file in bytes
    bytes = len(data)

    # Calculate the number of chunks to be created
    noOfChunks = bytes / chunkSize
    if (bytes % chunkSize):
        noOfChunks += 1

    # Initialize JSON text variable
    indexOfChunk = 0
    infoList = []

    # Received Credential Array
    receivedCredential = ["silencethakar", "silencenamu", "silencedeul"]

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
        print ("")
        print ("[CREATE] Created chunk file({0}) - '{1}'".format(indexOfChunk, fn1))

        if indexOfChunk < len(receivedCredential):
            credentialIndex = indexOfChunk
        else:
            credentialIndex = indexOfChunk % len(receivedCredential)

        # Input metadata of chunk file in dictionary
        dict = {}
        dict['fileName'] = inputFile
        dict['numberOfChunks'] = int(noOfChunks)
        dict['indexOfChunk'] = indexOfChunk
        dict['chunkName'] = fn1
        dict['account'] = receivedCredential[credentialIndex]

        # Input dictionary in List
        infoList.insert(indexOfChunk, dict)
        indexOfChunk += 1

    print ("[SYSTEM] Finish split file - Created chunk file '{0}'".format(indexOfChunk))

    return infoList


def uploadGoogledrive(infoList):

    uploadfilePath = os.getcwd() + "/cache/"

    for i in range(0, len(infoList)):
        fn1 = infoList[i]['chunkName']

        # upload_file(업로드된후 파일명, 파일설명, 파일타입, 실제 올릴 파일경로)
        uploadFile = googleDrive.upload_file(infoList[i]['account'], "%s" % fn1, '', '', uploadfilePath + fn1)

        infoList[i]['fileID'] = uploadFile['id']

        print ("[SYSTEM] Stored metadata of Chunk({0})- '{1}'".format(i, fn1))

        # Delete already uploaded chunk file
        if os.path.isfile(uploadfilePath+fn1):
            os.remove(uploadfilePath+fn1)
            print ("[DELETE] Remove already uploaded chunk file - '{0}'".format(fn1))

    return infoList


def createMetaData(infoList):

    # Convert list to dictionary
    serialized_dict = json.dumps(infoList)
    dictJSON = ast.literal_eval(serialized_dict)

    # Create metadata.json
    f = open('metadata.json', 'w')
    json.dump(dictJSON, f, indent=4)
    f.close()

    print ("\n[CREATE] Created metadata of '%s'" % infoList[0]['fileName'])



def downloadFile(metadataJSON, downFile):

    f = open(metadataJSON, "r")
    readJSON = json.load(f)
    f.close()

    noOfChunks = 0
    idx = 0

    print ("\n[SYSTEM] Read metadata\n")

    for item in range(0, len(readJSON)):
        if readJSON[item]['fileName'] == downFile:
            noOfChunks = readJSON[item]['numberOfChunks']
            googleDrive.downlaod_file(readJSON[item]['fileID'], "chunk%d" % idx)
            idx += 1
    print("")
    joinFiles(downFile, noOfChunks)


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


