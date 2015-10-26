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
#import credentials

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
    parser.add_argument("-enrol", "--sign_up_id")
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

    elif args.sign_up_id:
        indexOfAt = args.sign_up_id.index('@')
        id = args.sign_up_id[:indexOfAt]
        googleDrive.donate_id(id)

    elif args.revoke_account:
        indexOfAt = args.revoke_account.index('@')
        id = args.revoke_account[:indexOfAt]
        googleDrive.revoke_credentials(id)

    #file.uploadFile("cafebene.png")
    #file.uploadFile("MGMG_last.mp4")
    #googleDrive.view_file("0B-_r0Nosw-jtQlEtbkprS3RQM1k")
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
