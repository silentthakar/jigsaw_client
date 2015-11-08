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
import credentials

def main(argv):

    parser = argparse.ArgumentParser(
        prog='jigsaw',
        description='''
commands:
         [ -h ]                          Show Usage.
         [ -ls ]                         Print shared file list.
         [ -check ]                      Check metadata is correct or not.
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
    parser.add_argument("-check", action='store_true')
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
        googleDrive.print_all_file_list_of_all_account()

    elif args.check:
        file.checkFileID()

    # Upload command
    elif args.upload_file:
        file.uploadFile(args.upload_file)

    # Download command
    elif args.download_file:

        if args.download_file.rfind('/') < 10:
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

    # Upload file by name
    #file.uploadFile("connect.m4v")
    #file.uploadFile("MGMG.mp4")
    #file.uploadFile("cafebene.png")

    # delete file by name
    #file.deleteFile("MGMG.mp4")
    #file.deleteFile("cafebene.png")
    #file.deleteFile("connect.m4v")

    # Delete one account
    #googleDrive.delete_all_files_of_one_account("silencenamu")

    # Print file list in shared folder
    #googleDrive.print_file_list_of_all_account()

    # Print all file list in google drive
    #googleDrive.print_all_file_list_of_all_account()

    # Print to download
    #file.printFileList()

    # Download by string
    #file.downloadFileByString("MGMG.mp4/0B-oP1y2aj8zbOVltZ3lvaDVMXzg/0B057fk42Mk_MaFU4cXlHUXhvTjA/0B6YNyAA5dnxEVUhOZDZPeFZOcEU/0B6YNyAA5dnxEX3RBalJrS1F1SEU/0B057fk42Mk_MUWVTMkh6Rmc1dzQ/0B-oP1y2aj8zbWklPRzZMaTJZRmc/0B057fk42Mk_MeF93VzlmRXhLbk0/0B-oP1y2aj8zbU2h4cmZQSGlOd00/0B6YNyAA5dnxEWm5uQXM5Q1pfWk0/0B8bycS0tZho7RzhqcXl4VVQ5cE0/0B_JO2VwE5AvzWnpxZ2FfeW81MUU/0B4B4zy_rkOX7WUN2SUJGdlJVRjQ/0B4B4zy_rkOX7ZXp0TGJVQkprQ1U/0B8bycS0tZho7Zi05MzFBeVRRVXM/0B_JO2VwE5AvzczNGWDBpem9rRE0/0B_JO2VwE5AvzcTZldndEVF9IZU0/0B8bycS0tZho7dzdJMFlSRHhoZzA/0B4B4zy_rkOX7UnZoWV8wOFJzMkE/0B7c1bPYb5iI1Qzl6QndxQTNmZU0/0BxP01BqXwstTazVwY184dF9WUzQ/0B0NFyTSe2GFbZUpnb2R5Y2VOSzQ/0B0NFyTSe2GFbR0VJcE51b1E5R2s/0B7c1bPYb5iI1cEZlQUpPWjRwMjg/0BxP01BqXwstTR3VjOHZRemU5dnc/0BxP01BqXwstTYlFFdFhTXzB1aVk/0B7c1bPYb5iI1Q0ZqUGFlUEVxMkk/0B0NFyTSe2GFbWE1hMEZvSDhYUjg/0B-oP1y2aj8zbaXB1c3hWM3RQbms/0B057fk42Mk_MdzVpVkFsUkxKMGs/0B6YNyAA5dnxETVFUMkN6SnI4X0k/0B6YNyAA5dnxEd0xlbHdlLTJwcTg/0B057fk42Mk_MV05xRkh6S2N2WmM/0B-oP1y2aj8zbVG5Qem8yOGtURnM/0B057fk42Mk_MWGNuLXBmX0ozSjA/0B-oP1y2aj8zbbldzRXowZVRkaVk/0B6YNyAA5dnxEZVM1TC1XTkRhclE/0B8bycS0tZho7SElKaHdHZUU2b2c/0B_JO2VwE5AvzMHU0SGFQVEtyMW8/0B4B4zy_rkOX7bGZzTHRRZU5oWDA/0B4B4zy_rkOX7TndrcElnVTJkeVU/0B8bycS0tZho7MXVmWl84STllbG8/0B_JO2VwE5AvzNWFqQnNpT0syOEE/0B_JO2VwE5AvzSVZGOElQYm5DcVU/0B8bycS0tZho7VG5nOGZZQTFqZWM/0B4B4zy_rkOX7RWVnZkdLVXVPX3M/0B7c1bPYb5iI1QzUza1QxS2V3aXM/0BxP01BqXwstTMG5UWmVsd2xzV3M/0B0NFyTSe2GFbWTg4ZWZWcXBxaUU/0B0NFyTSe2GFbc01lX256QkUwLUE/0B7c1bPYb5iI1aWhLMXRncHlRRGc/0BxP01BqXwstTc3lfLXlQUjUxZnc/0BxP01BqXwstTZUtpUlBBXzNLY3c/0B7c1bPYb5iI1cWlSLWhadThMRVE/0B0NFyTSe2GFbWkVEZFlNOGhzbUE/0B-oP1y2aj8zbRWR6RzhYT3BJVGs/0B057fk42Mk_MMnAwTWRndTJTek0/0B6YNyAA5dnxEQ3ZRZThBUVROd1k/0B6YNyAA5dnxEQzhBVk1oTTdRb0E/0B057fk42Mk_MaWZoc0M2cml3ekU/0B-oP1y2aj8zbdGlDRUl5YkNYc2s/0B057fk42Mk_MQ0lFNDZCY2EyTDQ/0B-oP1y2aj8zbVFdUT1pNTWdIUkU/0B6YNyAA5dnxEa0wxN002MlF2ekE/0B8bycS0tZho7b2NSQjM0VzU0b0k/0B_JO2VwE5AvzVFU5NG9ZU2JGdWc/0B4B4zy_rkOX7MGJxTkI3NXd2WUU/0B4B4zy_rkOX7a3RjMHZ4RmRRU0E/0B8bycS0tZho7RHJzN3lBWVhoOGc/0B_JO2VwE5AvzTXVIVTBjR0tTLVk/0B_JO2VwE5Avzc2RWWFQ1RFB4dFE/0B8bycS0tZho7bllsRklYZFlzM0E/0B4B4zy_rkOX7UFlidVVUeFNzLVk/0B7c1bPYb5iI1cHd6UFJZNXV5ZWc/0BxP01BqXwstTT0VOQ3NEdEJhRzA/0B0NFyTSe2GFbTnJoeU1wVmowTGM/0B0NFyTSe2GFbUzBpMlN2b05vU1E/0B7c1bPYb5iI1aEt0ZDFOZkxDRlU/0BxP01BqXwstTYlpKTXl2eE90OFk/0BxP01BqXwstTeXpFYnFjNFNJb2M/0B7c1bPYb5iI1S1FDMF9XS2Z4Nlk/0B0NFyTSe2GFbZ1c0STNkb0JSNTQ/0B-oP1y2aj8zbdGlaYXJVekN4OHM/0B057fk42Mk_MSVZHUUNycVBva1k/0B6YNyAA5dnxEczBieDZlTW5XYXM/0B6YNyAA5dnxEaUZ4R2lxM25icUk/0B057fk42Mk_MaHBCQk14cFk4TWM/0B-oP1y2aj8zbcG1yb04weUNaUWc/0B057fk42Mk_MRGMzZUJsaUlVMVE/0B-oP1y2aj8zbRGlTWlZuRURKTXc/0B6YNyAA5dnxESWs5Z0FYbHJrNnM/0B8bycS0tZho7MTFZckZWMGs1Q0k/0B_JO2VwE5Avzc0tqWXJlVFBoZjA/0B4B4zy_rkOX7OWNGWFg4NE1TcE0/0B4B4zy_rkOX7S0VsS0dIVlpvaEk/0B8bycS0tZho7SW1jOHRnX01yUjA/0B_JO2VwE5AvzdW9CYnM0eHJDMEE/0B_JO2VwE5AvzbFlwNk8tLTlBWUk/0B8bycS0tZho7YzhYOVk0eHN1QWs/0B4B4zy_rkOX7amxGVVRhTDIwU28/0B7c1bPYb5iI1ZFZzZlc0a3I0bTA/0BxP01BqXwstTRTZZS1ZHYnFqWDg/0B0NFyTSe2GFbaGtXV2VqOUxzRDA/0B0NFyTSe2GFbS1dIbUdkX0RYM0U/0B7c1bPYb5iI1VTFFN2E1SVJ2ZzA/0BxP01BqXwstTQVk1a2RndXBXczg/0BxP01BqXwstTMzlWV1RLTktIc0k/0B7c1bPYb5iI1YWZOMGtIb3dqUGc/0B0NFyTSe2GFbcnY1dDhJSEJqOXM")
    #file.downloadFileByString("")

    #file.checkFileID()

    #googleDrive.revoke_credentials("silencethakar")

    #credentials.get_credentials_by_id("silencedeul")


if __name__ == '__main__':
    main(sys.argv)

