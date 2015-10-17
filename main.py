#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import argparse
#from docopt import docopt
#from schema import Schema, SchemaError, Optional

LS = """ usage: basic.py ls [option]

    -h --help         Show this screen.
"""

DELETE = """ usage: basic.py download [option]

    -h --help         Show this screen.
"""

UPLOAD = """ usage: basic.py upload [option] [<name>]
    -h --help         Show this screen.
"""

DOWNLOAD = """ usage: basic.py download [option] [<name>]

    -h --help         Show this screen.
"""


"""
def jigsaw(args):
    receivedCredential = ["silencethakar", "silencenamu", "silencedeul"]

    if args['ls']:
        googleDrive.read_file_list_of_all_account(receivedCredential)

    elif args['delete']:
        googleDrive.delete_all_files_of_all_account(receivedCredential)

    elif args['upload']:
        file.uploadFile('{0}'.format(args['<uname>']))

    elif args['download']:
        file.downloadFile("metadata.json", '{0}'.format(args['<dname>']))

    #if args['--caps']:
    #    output = output.upper()
    #print(output)

if __name__ == '__main__':
    arguments = docopt(__doc__, help=False, options_first=False, version=None)
    print (arguments)

    schema = Schema({
        Optional('ls'): bool,
        Optional('delete'): bool,
        Optional('upload'): bool, '<uname>': str,
        Optional('download'): bool, '<dname>': str,
        Optional('ls'): bool,
        Optional('--help'): bool
    })

    def validate(args):
        try:
            args = schema.validate(args)
            return args
        except SchemaError as e:
            exit(e)

    if arguments['<command>'] == 'ls':
        jigsaw(validate(docopt(LS)))
    elif arguments['<command>'] == 'delete':
        jigsaw(validate(docopt(DELETE)))
    elif arguments['<command>'] == 'upload':
        jigsaw(validate(docopt(UPLOAD)))
    elif arguments['<command>'] == 'download':
        jigsaw(validate(docopt(DOWNLOAD)))
    else:
        exit("{0} is not a command. See 'options.py --help'.".format(arguments['<command>']))
"""

def main():

    receivedCredential = ["silencethakar", "silencenamu", "silencedeul"]

    googleDrive.read_file_list_of_all_account(receivedCredential)

    file.uploadFile("cafebene.png")

    googleDrive.read_file_list_of_all_account(receivedCredential)

    file.downloadFile("metadata.json", "cafebene.png")

    googleDrive.delete_all_files_of_all_account(receivedCredential)


if __name__ == '__main__':
    main()
