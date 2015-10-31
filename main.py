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
    #googleDrive.delete_all_files_of_all_account()

    # Upload file
    #file.uploadFile("connect.m4v")
    #file.uploadFile("MGMG.mp4")
    #file.uploadFile("cafebene.png")
    file.uploadFile("connect.m4v")

    # Print all file list
    #googleDrive.print_file_list_of_all_account()

    # Print to download
    #file.printFileList()

    # Download by string
    #file.downloadFileByString("MGMG.mp4/0B5iptnvBTi5SNGxJa01jd1pNU2M/0B-oP1y2aj8zbcWw4Wk93NDIzQVk/0B6YNyAA5dnxEYk5nUDMzSGhhY2M/0B057fk42Mk_McjRGOXUxd0E5a2M/0B8bycS0tZho7Vnd1b0FOSExpNm8/0B4B4zy_rkOX7TV9WNDJVX2hMd00/0B_JO2VwE5AvzRFNfbnN5OTZEenM/0B7c1bPYb5iI1bXRnc1dGWGRncEU/0B0NFyTSe2GFbUXRTQXFoWGtEUHc/0B5iptnvBTi5SOUNzM2haYVVWNzA/0B-oP1y2aj8zbZXZtOHlSOVFIZlk/0B6YNyAA5dnxES2VYaFFXYnA5WE0/0B057fk42Mk_MZEdLdm1EVVN3cGM/0B8bycS0tZho7U0ZRTU02WkpMRXM/0B4B4zy_rkOX7bFk2ZVJOak5NVkE/0B_JO2VwE5AvzcDVWZGRQTUNWYkE/0B7c1bPYb5iI1QjdJSVUxem1wYXc/0B0NFyTSe2GFbYWNyVkJDTG5Helk/0B5iptnvBTi5SdWVsWDhWbTBHbU0/0B-oP1y2aj8zbWXA1VXNjWjJLeFU/0B6YNyAA5dnxEOGZKRUlWNDJKYnM/0B057fk42Mk_MdFRSa2Q3d2hzV2s/0B8bycS0tZho7RFJCbHVRQ0N2cnM/0B4B4zy_rkOX7MmN6VHo0X21hbjg/0B_JO2VwE5AvzeGFQMk5ncTFFWkE/0B7c1bPYb5iI1M2huVVNIbjh0THM/0B0NFyTSe2GFbVkx0ZUJnV3pmTFk/0B5iptnvBTi5Sam9pcVBYdkJqcmc/0B-oP1y2aj8zbVW1vUGZVX1VOQ00/0B6YNyAA5dnxETFFYN0s2a2Zqc28/0B057fk42Mk_MczhacThWUHVsN1U/0B8bycS0tZho7aWRjLXZxYTItWkE/0B4B4zy_rkOX7aE4xaEQxaEhONk0/0B_JO2VwE5Avzb0VvS0prTnFHQlE/0B7c1bPYb5iI1OEdoaFZ2MDVSb2s/0B0NFyTSe2GFbbW43Nmp2LUx3ekk")

    #googleDrive.view_file("0B-_r0Nosw-jtQlEtbkprS3RQM1k")


    """
    googleDrive.revoke_credentials("silencethakar")
    googleDrive.revoke_credentials("silencenamu")
    googleDrive.revoke_credentials("silencedeul")
    googleDrive.revoke_credentials("silencesoop")
    """

if __name__ == '__main__':
    main(sys.argv)
