Jigsaw Puzzle [Client]
==========================

command line tools for share file using google drive

## Setup

1. Install jigsaw-client. `pip install jigsaw-client`
2. Clone this project

Tested with Python 3.5 only.


## Quick Start

1. Donate google account
	> jigsaw -enrol [ YOUR_GOOGLE_ACCOUNT ]
2. Check quota of your google account
	> jigsaw -df
3. Upload file
 	> jigsaw -put [ UPLOAD_FILE_NAME ]
3. Update upload file list
	> jigsaw -check
4. Print string to download file
	> jigsaw -ls
5. Download file
	> jigsaw -get [ STRING_TO_DOWNLOAD ]
6. Delete upload file
	> jigsaw -rm [ FILE_NAME_FOR_DELETE ]


## Usage

```
$ ./jigsaw.py -h
usage: jigsaw [-h] [-ls] [-df] [-r] [-l] [-check] [-put UPLOAD_FILE]
              [-get DOWNLOAD_FILE] [-rm DELETE_FILE] [-la FILE_LIST_OF_ID]
              [-enrol ENROL_ID] [-ra REMOVE_FILE_OF_ID] [-vk REVOKE_ACCOUNT]

commands:
         [ -h ]                          Show Usage.
         [ -ls ]                         Print shared file list.
         [ -df ]                         Print used quota of google drive.
         [ -check ]                      Check metadata is correct or not.
         [ -put <file name> ]            Upload file on google drive.
         [ -get <file name> ]            Download file on google drive.
         [ -rm <file name> ]             Delete file on google drive.
         [ -enrol <account name> ]       Get permission to get credential.
         [ -vk <account name> ]          Revoke credential

optional arguments:
  -h, --help            									Show this help message and exit
  -r														Delete all file on all of google drive
  -l														Print file list on all of google drive
  -la FILE_LIST_OF_ID, --file_list_of_id FILE_LIST_OF_ID	Print file list on one of google drive
  -ra REMOVE_FILE_OF_ID, --remove_file_of_id REMOVE_FILE_OF_ID Remove files on one of google drive
```
