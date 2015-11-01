#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
# -*- coding: utf-8 -*-

# Set global executable instruction
# chmod 744 main.py
# ln -s "/Users/yeonhong/Documents/JigsawPuzzle/jigsaw_client/main.py" /usr/local/bin/jigsaw

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


    # Print credential list
    #googleDrive.get_credentials_list()

    # Delete all
    googleDrive.delete_all_files_of_all_account()

    # Upload file by name
    #file.uploadFile("connect.m4v")
    #file.uploadFile("MGMG.mp4")
    #file.uploadFile("cafebene.png")


    # delete file by name
    #file.deleteFile("MGMG.mp4")
    #file.deleteFile("cafebene.png")

    # Print file list in shared folder
    #googleDrive.print_file_list_of_all_account()

    # Print all file list in google drive
    #googleDrive.print_all_file_list_of_all_account()

    # Print to download
    #file.printFileList()

    # Download by string
    #file.downloadFileByString("MGMG.mp4/0B5iptnvBTi5SckoteVhORVpaSlU/0B-oP1y2aj8zbeXQ1ZnNDVVRwWnc/0B6YNyAA5dnxEb0pxYWdBVENQRkU/0B057fk42Mk_MR0NEaEtQUzU0LTQ/0B8bycS0tZho7Q3c2TF91QkNFQmc/0B4B4zy_rkOX7SFNNa0RpVG9ZcTA/0B_JO2VwE5AvzQjZTNmlOdFhlTkE/0B7c1bPYb5iI1QV9fZjdhS0w0UXc/0B0NFyTSe2GFbdERkRUdjb1RXTVk/0B5iptnvBTi5SY1FzbWtpLWJtY00/0B-oP1y2aj8zbYzFnc0piZ1ZSaDA/0B6YNyAA5dnxENlo1VG53eE9lNW8/0B057fk42Mk_MWEZwWFczRl8tRW8/0B8bycS0tZho7cE40WjUzX1l6aVE/0B4B4zy_rkOX7NmF5R3l6M0VMSEE/0B_JO2VwE5AvzVkQ0M1RHRm5scFU/0B7c1bPYb5iI1amNlRExTbjc0Qkk/0B0NFyTSe2GFbRGVqWXA4aFBfQmc/0B5iptnvBTi5SZ0I3bERSamJ4ZkU/0B-oP1y2aj8zbTHhGcFZmRmJsTzQ/0B6YNyAA5dnxEeGxheWxLMFVabTQ/0B057fk42Mk_MRERWS2RESzBZRTg/0B8bycS0tZho7UkZ4LWd6Wk1GQ3c/0B4B4zy_rkOX7aFp0SFpsMVVhNlE/0B_JO2VwE5AvzRWRFN0RiZ253YU0/0B7c1bPYb5iI1TWk5dXlEM3JBdGM/0B0NFyTSe2GFbY0JqSGFZNVRsOTg/0B5iptnvBTi5SbF9rNGhqZ3I0QXc/0B-oP1y2aj8zbMlVvbVZZVm10TFU/0B6YNyAA5dnxESVZBZUVpRmxzX2M/0B057fk42Mk_MQ1F4cEZiR3gzOGc/0B8bycS0tZho7bHVKS0t6YnVWRnc/0B4B4zy_rkOX7Y1R0TFpTM2tYa1E/0B_JO2VwE5AvzajhGVzB4blRpd0k/0B7c1bPYb5iI1ZXdhUmI0bDNWVXM/0B0NFyTSe2GFbOXZSdzNQZHQ5NHM")

    #file.deleteFile("cafebene.png")

    #googleDrive.view_file("0B-_r0Nosw-jtQlEtbkprS3RQM1k")


    """
    googleDrive.revoke_credentials("silencethakar")
    googleDrive.revoke_credentials("silencenamu")
    googleDrive.revoke_credentials("silencedeul")
    googleDrive.revoke_credentials("silencesoop")
    """

if __name__ == '__main__':
    main(sys.argv)
