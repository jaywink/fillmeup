#!/usr/bin/env python

import sys,getopt,FMURunner

def main(arguments):
    version = "0.8 alpha"
    __doc__ = """ 
****************************
*        FILL ME UP        *
****************************
         
Version: 
    """+version+"""
    Powered by Python 2.6 & PyQt 4.5
    Packaged with PyInstaller 1.3
    
Usage:
    FillMeUp [options] [target path]
        (only one target path can be specified and the folder must exist)
    
Options:
    -h  --help      Display this help
    -p  --path      Set file collection path (subfolders are always included)
    -f  --file-group    Set file type group
    -t  --file-type     Set file extensions (comma separated list, for ex. "jpg,gif,ico")
    -s  --space     Set amount of MB to be filled
    -c  --cmdline       Run in command line mode
    -g  --generate      Generate only, don't copy (relevant only in command line mode)

File Groups:
    MUSIC   :   ['mp3','wma','ogg','wav','flac']
    DOCUMENT:   ['txt','doc','xls']
    IMAGE   :   ['jpg','gif','png']

Disclaimer:
    Use at your own risk! Author takes no responsibility for any damages to 
    anything caused by this software

Author:
    Jason Robinson
    http://www.basshero.org
    jaywink@basshero.org
    """
    settings = {'version':version,'doc':__doc__}
    # parse command line options
    try:
        opts, args = getopt.getopt(arguments[1:], "gchp:t:f:s:", ["help","cmdline","path=","file-type=","space=","generate"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    if len(args) == 0:
        args = ['']
    settings["path"] = ''
    settings["file-types"] = []
    settings["space"] = 0
    settings["gui"] = True
    settings["targetNeeded"] = True
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o in ("-p","--path"):
            settings["path"] = a
            print "Path set as",settings["path"]
        elif o in ("-f","--file-group"):
            settings["file-types"] = a
            print "File types set as",settings["file-types"]
        elif o in ("-t","--file-type"):
            settings["file-types"] = a
            print "File type set as",settings["file-types"]
        elif o in ("-s","--space"):
            if a.isdigit():
                settings["space"] = int(a)*1048576
                print "Space set to ",settings["space"],"bytes"
            else:
                print "Space (mb) must be numeric"
                sys.exit(1)
        elif o in ("-c","--cmdline"):
            settings["gui"] = False
        elif o in ("-g","--generate"):
            settings["targetNeeded"] = False
    # app main loops
    if settings["gui"] == True:
        # create a gui object
        import FMUGUI
        if settings["targetNeeded"] == True:
            settings["targetNeeded"] = False
        print "Compiling file list with given arguments and then launching GUI..."
        if len(args) > 0:
            gui = FMUGUI.GUIApp(args[0],settings)
        else:
            gui = FMUGUI.GUIApp('',settings)
    else:
        # command line
        print "Compiling file list with given arguments..."
        runner = FMURunner.Runner(settings,args[0])
        runner.doConsole()
            
if __name__ == "__main__":
    main(sys.argv)
