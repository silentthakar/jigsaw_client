#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
# -*- coding: utf-8 -*-

# Set global executable instruction
# chmod 744 main.py
# ln -s "/Users/yeonhong/Documents/MyDropBox/jigsaw_client/main.py" /usr/local/bin/jigsaw

"""usage: jigsaw [--help] <command> [<args>...]

options:
  -h --help         Show this screen.
  --version         Show the version.
  -a                Delete all file on google drive.

commands:
    ls              Print file list
    delete          Delete files on google drive
    upload          Upload file on google drive.
    download        Download file on google drive.

"""

import googleDrive
import file
import sys
import argparse
#import result_requester
import credentials

def main(argv):

    #result_requester.app.run('0.0.0.0', 9991, debug=False)


    parser = argparse.ArgumentParser(
        prog='jigsaw',
        description='''
commands:
         [ -h ]                          Show Usage.
         [ -ls ]                         Print shared file list.
         [ -put <file name> ]            Upload file on google drive.
         [ -get <file name> ]            Download file on google drive.
         [ -rm <file name> ]             Delete file on google drive.
         [ -enrol <account name> ]       Get permission to get credential.
         [ -vk <account name> ]          Revoke credential''',

        formatter_class=argparse.RawDescriptionHelpFormatter)

    #parser.add_argument('-l', "--list_id", nargs="+") -> use args list
    parser.add_argument("-ls", action='store_true')
    parser.add_argument("-r", action='store_true')
    parser.add_argument("-l", action='store_true')
    parser.add_argument("-put", "--upload_file")
    parser.add_argument("-get", "--download_file")
    parser.add_argument("-rm", "--delete_file")
    parser.add_argument("-la", "--file_list_of_id")
    parser.add_argument("-enrol", "--enrol_id")
    parser.add_argument("-ra", "--remove_file_of_id")
    parser.add_argument("-vk", "--revoke_account")

    #parser.parse_args('-h'.split())R
    args = parser.parse_args()

    #print (args)

    if args.ls:
        file.printFileList()

    elif args.r:
        googleDrive.delete_all_files_of_all_account()

    elif args.l:
        googleDrive.print_file_list_of_all_account()

    # Upload command
    elif args.upload_file:
        file.uploadFile(args.upload_file)

    # Download command
    elif args.download_file:

        if args.download_file.rfind('.') < 5:
            file.downloadFile(args.download_file)
        else:
            file.downloadFileByString(args.download_file)

    elif args.delete_file:
        file.deleteFile(args.delete_file)

    # List - Print file list in google drive
    elif args.file_list_of_id:
        googleDrive.print_files_in_shared_folder(args.file_list_of_id)

    elif args.remove_file_of_id:
        googleDrive.delete_all_files_of_one_account(args.remove_file_of_id)

    elif args.enrol_id:
        indexOfAt = args.enrol_id.index('@')
        id = args.enrol_id[:indexOfAt]
        googleDrive.donate_id(id)

    elif args.revoke_account:
        indexOfAt = args.revoke_account.index('@')
        id = args.revoke_account[:indexOfAt]
        googleDrive.revoke_credentials(id)


    #googleDrive.get_credentials_list()
    #list = file.splitFile("cafebene.png")
    #print (list)


    #googleDrive.delete_all_files_of_all_account()
    #file.uploadFile("W3.pdf")
    googleDrive.print_file_list_of_all_account()
    #file.printFileList()
    #file.downloadFileByString("ApplePi-Baker 2.zip/0B-oP1y2aj8zbeDlBcEdoTEI5bkU/0B6YNyAA5dnxEclBtNk9KVDJYT2s/0B-oP1y2aj8zbZlZfYVRyZkg0N0U/0B6YNyAA5dnxEVC1PV0hLd1d1clU/0B-oP1y2aj8zbVERkRWVzangwVXc/0B6YNyAA5dnxERTJXZVkxYjNQY0U/0B-oP1y2aj8zbMVBNcUtRUWxsZGc/0B6YNyAA5dnxEQW0zbzdoYjBaWk0/0B-oP1y2aj8zbS2ZOUUhESUhmcEU/0B6YNyAA5dnxEX0pmaE5wN3F3Zk0/0B-oP1y2aj8zbSzFNRHA1LVJUZkk")
    #file.uploadFile("MGMG.mp4")
    #file.downloadFileByString(" MGMG_last.mp4/0B-oP1y2aj8zbSURFSnNFaUNMYlU/0B6YNyAA5dnxEU21wQTNRMlQzWm8/0B-oP1y2aj8zbXzNZZTV4N1lkQjQ/0B6YNyAA5dnxEZEN2cEJZR0dsN2c/0B-oP1y2aj8zbbG1Hd2V0RTRWR0k/0B6YNyAA5dnxEMUxhTkZQNEtSMzQ/0B-oP1y2aj8zbTEgyTmpZWU16UlE/0B6YNyAA5dnxEM0llU0pCWGtPeVk/0B-oP1y2aj8zbdENxakNUa3RZZmc/0B6YNyAA5dnxEejdjbkpsRzdTcUk/0B-oP1y2aj8zbZjQ3MEJUY2FDT1E/0B6YNyAA5dnxEcnIzamdwZUVNYjA/0B-oP1y2aj8zbQlNESmRuR2FrODQ/0B6YNyAA5dnxEOEw0bktDZldyWms/0B-oP1y2aj8zbRzRkOXJPaXAtSGc/0B6YNyAA5dnxETGVkV3g1QlZRbkU/0B-oP1y2aj8zbM1AzcTZvTks4alE/0B6YNyAA5dnxEQUJNS2pROUtFZTA/0B-oP1y2aj8zbRFQwN29qMVhPbms/0B6YNyAA5dnxEcWg3SnkxZk5rSkU/0B-oP1y2aj8zbZXhjQ1dXTm82SmM/0B6YNyAA5dnxEYmhFemtQdjF6SjQ/0B-oP1y2aj8zbTXdvZXFaTVZ3Wk0/0B6YNyAA5dnxEQVZHaEdHbzBmUVk/0B-oP1y2aj8zbSjBPXzRZRGc0NTg/0B6YNyAA5dnxEVWVyTXVpRWJrWlU/0B-oP1y2aj8zbZkd5SzFEQWRhaG8/0B6YNyAA5dnxEcU5POFJGRnNEdXM/0B-oP1y2aj8zbcHFYdHJBRVNKTHM/0B6YNyAA5dnxEbFJCaEtmeUttajA/0B-oP1y2aj8zbendRdFBKUTh0VFk/0B6YNyAA5dnxEa1Y1SXJOMmR6cDg/0B-oP1y2aj8zbaWNhVUNTcFMxWkU/0B6YNyAA5dnxEMXgyLVB2UDR1LVE/0B-oP1y2aj8zbYm9wcm1ZVHF4dXM/0B6YNyAA5dnxEMFNWRGNSOTRXdFE/0B-oP1y2aj8zbSEdQcmVXdUFIdkE")
    # file.uploadFile("cafebene.png")
    # file.uploadFile("MGMG_last.mp4")
    # googleDrive.view_file("0B-_r0Nosw-jtQlEtbkprS3RQM1k")
    """

    googleDrive.read_file_list_of_all_account(receivedCredential)

    file.uploadFile("cafebene.png")

    googleDrive.read_file_list_of_all_account(receivedCredential)

    file.downloadFile("metadata.json", "cafebene.png")

    googleDrive.delete_all_files_of_all_account(receivedCredential)
    """

    """"
    googleDrive.revoke_credentials("silencethakar")
    googleDrive.revoke_credentials("silencenamu")
    googleDrive.revoke_credentials("silencedeul")
    googleDrive.revoke_credentials("silencesoop")
        """

if __name__ == '__main__':
    main(sys.argv)
