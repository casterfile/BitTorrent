#!/usr/bin/env python

# Written by Henry 'Pi' James and Bram Cohen
# multitracker extensions by John Hoffman
# see LICENSE.txt for license information

import sys
import os
import getopt
from BitTornado.bencode import bencode, bdecode

def main(argv):
    program, ext = os.path.splitext(os.path.basename(argv[0]))
    usage = """Usage: %s <http-seeds> file1.torrent [file2.torrent...]

  Where:
    http-seeds = list of seed URLs, in the format:
        url[|url...] or 0
            if the list is a zero, any http seeds will be stripped.
""" % program

    try:
        opts, args = getopt.getopt(argv[1:], "hv",
                        ("help","verbose"))
    except getopt.error, msg:
        print msg
        return 1

    if len(args) < 2:
        print usage
        return 2
    
    http_seeds = None
    if args[0] != '0':
        http_seeds = args[0].split('|')

    verbose         = False

    for opt, arg in opts:
        if opt in ('-h','--help'):
            print usage
            return 0
        elif opt in ('-v','--verbose'):
            verbose = True

    for fname in args[1:]:
        with open(fname, 'rb') as metainfo_file:
            metainfo = bdecode(metainfo_file.read())

        if 'httpseeds' in metainfo:
            if verbose:
                print 'old http-seed list for %s: %s' % (fname,
                        '|'.join(metainfo['httpseeds']))
            if http_seeds is None:
                del metainfo['httpseeds']
        
        if http_seeds is not None:
            metainfo['httpseeds'] = http_seeds
        
        with open(fname, 'wb') as metainfo_file:
            metainfo_file.write(bencode(metainfo))

if __name__ == '__main__':
    sys.exit(main(sys.argv))