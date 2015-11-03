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
    #file.downloadFileByString("MGMG.mp4/0B5iptnvBTi5SeFViYWVrb00yMUk/0B-oP1y2aj8zbWkdQQWYzdThWNnM/0B6YNyAA5dnxERGx1UnlkSHdRUTg/0B-oP1y2aj8zbbnI5dndtN1BHMnM/0B5iptnvBTi5SWDRBdzB4VElmV28/0B6YNyAA5dnxEdmdtenBfeUduYzQ/0B6YNyAA5dnxEb2FhSk51QmF2cTA/0B-oP1y2aj8zba0I5a1UwRVZKVms/0B5iptnvBTi5SSjdTam5NMkNUU28/0B057fk42Mk_MV0RRcHBvTm9zSlE/0B8bycS0tZho7dDh1OXhsczlBNTg/0B4B4zy_rkOX7Z1pXODJVZzRScUU/0B8bycS0tZho7ZnNoVXNIOGF1Y1E/0B057fk42Mk_MZkNrQ3JFeUNWMVU/0B4B4zy_rkOX7VHBFdUpFNUZ1RDA/0B4B4zy_rkOX7U2N3LXR4MHktWTg/0B8bycS0tZho7VXA2NDNQdnpKTkk/0B057fk42Mk_MYUdEa0ZETUlUQzg/0B_JO2VwE5Avzc3BJdWRLTERKR1U/0B0NFyTSe2GFbNkdWcGUtZFppMnc/0B7c1bPYb5iI1QnNCdmRVS1I4SG8/0B7c1bPYb5iI1SlphNGJSVzNPOWc/0B0NFyTSe2GFbTTZCemFwTXFQUlU/0B_JO2VwE5AvzWFRlZEZlbUpoWXM/0B0NFyTSe2GFbNHpXMnJvRjNQa0U/0B7c1bPYb5iI1bm9JUDkyNkFuWTg/0B_JO2VwE5AvzU3ZoQkRRekdrU3c/0B5iptnvBTi5SNlptT2FRWU5OdTg/0B-oP1y2aj8zbbVdmVVpqU2tJNHc/0B6YNyAA5dnxESXNuMEpaMndTc0E/0B-oP1y2aj8zbaDJNRFR2XzdOblU/0B5iptnvBTi5SOVpIZUV4empJVDg/0B6YNyAA5dnxENm9sSkVsV2k3V2M/0B6YNyAA5dnxEZXBTRzJPdkYwdU0/0B-oP1y2aj8zbYmNCMFJIbDhVNjA/0B5iptnvBTi5SNldJa0RacS1KMmM/0B057fk42Mk_MakIwdGw1ZG9EYk0/0B8bycS0tZho7LVZNc1BjR1NKY28/0B4B4zy_rkOX7ck13T21hcWhjUEk/0B8bycS0tZho7U1l3ZWRFaGVqekE/0B057fk42Mk_MX2xBVkYwb2g1c00/0B4B4zy_rkOX7eGtjZXpJOEZHSU0/0B4B4zy_rkOX7bjNmTUhxa2RSUVE/0B8bycS0tZho7OWFDYmtYRE4yY3c/0B057fk42Mk_MS256Q3c0elcxNGc/0B_JO2VwE5AvzVVZseUJScGxiTVE/0B0NFyTSe2GFbTktRTnB5eGFSWms/0B7c1bPYb5iI1cERyd3NENDczb0E/0B7c1bPYb5iI1VGJwVVk2SVVpcm8/0B0NFyTSe2GFbcy1sMV85dlVpWlU/0B_JO2VwE5AvzLW9uZDBxdm5zbHM/0B0NFyTSe2GFbcUlNM09QdWJKYlk/0B7c1bPYb5iI1enZoeVdNNG5WZDg/0B_JO2VwE5AvzbklfNHVVX3pWZ2M/0B5iptnvBTi5SRVdwNlhUR1lSX0k/0B-oP1y2aj8zbMVJuZE80X0tGLTA/0B6YNyAA5dnxENG9NLTdyYlQwWWM/0B-oP1y2aj8zbNTNnSkQtX2JORGs/0B5iptnvBTi5SN3hVT3Q5SWF6RkU/0B6YNyAA5dnxERmlXaDRmTnFKVGc/0B6YNyAA5dnxESWRBNElXVy1iVzA/0B-oP1y2aj8zbTjZ4dUZMQ1ZnRWs/0B5iptnvBTi5SQXgySjB0TlNLMUU/0B057fk42Mk_MSFFVeUtLSFRrQ1k/0B8bycS0tZho7OUkzUEd3emJvNEE/0B4B4zy_rkOX7SVRIM1Noa3ByRTA/0B8bycS0tZho7cXlGdG5aQUZqbjA/0B057fk42Mk_MOVF1d3NxV3UwOUk/0B4B4zy_rkOX7c04wLTExSVhlMEk/0B4B4zy_rkOX7V19vZE52SzIxdzg/0B8bycS0tZho7TnZlWDVkb1ptLVU/0B057fk42Mk_Md1lqdC1XaS1PMHc/0B_JO2VwE5AvzZlpuRm1fSlJtNlE/0B0NFyTSe2GFbTl9CR1FqTzYtS3M/0B7c1bPYb5iI1RzQ0dFFNLVVpd2s/0B7c1bPYb5iI1WU1OTlNRbGdBVHc/0B0NFyTSe2GFbYWVGTVFReElfTGM/0B_JO2VwE5AvzS1VyaWI0Z1YxMUU/0B0NFyTSe2GFbTkRhT3A2Z2t2S00/0B7c1bPYb5iI1dTFNTlk5NmpuMXM/0B_JO2VwE5AvzOU9IRHNFVHNBRDg/0B5iptnvBTi5SdXluSURRc0IxcU0/0B-oP1y2aj8zbemZRTW1BTmN2bHM/0B6YNyAA5dnxESXJDV1kwS0dyWG8/0B-oP1y2aj8zbMVB0T21IcFVYbG8/0B5iptnvBTi5SNWdxeXZ0ay1KM1k/0B6YNyAA5dnxEbjZiUDdMZ0ZFWlE/0B6YNyAA5dnxEb25rXzMxSkk2dVE/0B-oP1y2aj8zbbFR2dFNNUDhGaEE/0B5iptnvBTi5SamlyX3VxRTFPZHM/0B057fk42Mk_MY0xvemdoeDRTQVE/0B8bycS0tZho7QnNHOF9PU1NuckE/0B4B4zy_rkOX7NXpqd0hRak5aOUU/0B8bycS0tZho7eUhaNVlVSnZfV1E/0B057fk42Mk_Ma0lPUlpDM213WXc/0B4B4zy_rkOX7QTZHWV85VFk4Rk0/0B4B4zy_rkOX7MmFLVmpYOWMwVUk/0B8bycS0tZho7RXBUaWZUMGRvV28/0B057fk42Mk_MZXRJb3lSLTg5dTg/0B_JO2VwE5AvzWHNqd2JiOUhMWm8/0B0NFyTSe2GFbdW1rZWs4Mm4xdkk/0B7c1bPYb5iI1SjRyWGg4UGdSaWc/0B7c1bPYb5iI1MjczZm9jZE9KdnM/0B0NFyTSe2GFbZXpmbkV1MmduaTA/0B_JO2VwE5AvzaVhiMHJzZWlNUEk/0B0NFyTSe2GFbc0JCeUI0OUxHZTA/0B7c1bPYb5iI1UjhfNGw5S1RZdmM/0B_JO2VwE5AvzZjVwMHROLVJMYzA")

    #file.deleteFile("cafebene.png")

    #googleDrive.view_file("0B-_r0Nosw-jtQlEtbkprS3RQM1k")

    #googleDrive.delete_all_files_of_one_account("silencenamu")

    """
    googleDrive.revoke_credentials("silencethakar")
    googleDrive.revoke_credentials("silencenamu")
    googleDrive.revoke_credentials("silencedeul")
    googleDrive.revoke_credentials("silencesoop")
    """

if __name__ == '__main__':
    main(sys.argv)
