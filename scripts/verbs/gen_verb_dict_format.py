# -*- coding=utf-8 -*-
#************************************************************************
# $Id: conjugate.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#  This file is the main file to execute the application in the command line
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/


import sys
import re
import string
import argparse
import os

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../support/'))
import pyarabic.araby as araby
from libqutrub.mosaref_main import *
import verbdict_functions as vdf
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"

# Limit of the fields treatment

MAX_LINES_TREATED=1100000;



def usage():
# "Display usage options"
    print("(C) CopyLeft 2016, %s"%AuthorName)
    print("Usage: %s -f filename [OPTIONS]" % scriptname)
#"Display usage options"
    print("\t[-h | --help]\t\toutputs this usage message")
    print("\t[-v | --version= dataversion]\tset Generated data version")
    print("\t[-f | --file= filename]\tinput file to %s"%scriptname)
    print("\t[-o | --output= format]\toutput file format %s"%scriptname)
    print("\t[-l | --limit= limit_ number]\tthe limit of treated lines %s"%scriptname)
    print("\r\nN.B. FILE FORMAT is descripted in README")
    print("\r\nThis program is licensed under the GPL License\n")


def grabargs2():
#  "Grab command-line arguments"
    fname = ''
    limit=MAX_LINES_TREATED;
    output = "csv"
    version = ""
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:v:f:l:o:",
                               ["help", "version=", "file=","limit=", "output="],)
    except getopt.GetoptError:
        usage()
        sys.exit(0)
    for o, val in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-v", "--version"):
            version = val
        if o in ("-o", "--output"):
            output = val.lower()
        if o in ("-f", "--file"):
            fname = val
        if o in ("-l", "--limit"):
            try:
                limit = int(val);
            except:
                limit=MAX_LINES_TREATED;

            
    return fname,limit, output, version

def grabargs():
    parser = argparse.ArgumentParser(description='Convert Noun dictionary to other format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outformat", nargs='?',
    help="output format(csv, sql, python, xml)", metavar="FORMAT")

    parser.add_argument("-v", dest="version", nargs='?',
    help="Release version", metavar="Version")
    
    parser.add_argument("--header",dest="header", type=bool, nargs='?',
                        const=True, 
                        help="add header")    

    parser.add_argument("-l",dest="limit", type=int, nargs='?',
                         help="the limit of treated lines")
    args = parser.parse_args()
    return args
def factory(output_format, version):
    import csvdict
    mydict = csvdict.CsvDict(version)
    if output_format == "sql":
        import sqldict
        mydict = sqldict.SqlDict(version);
    elif output_format == "xml":
        import xmldict
        mydict = xmldict.XmlDict(version);
    elif output_format == "stardict":
        import stardict
        mydict = stardict.StarDict(version);        
    elif output_format == "spell":
        import spelldict
    elif output_format == "tags":
        import tagsdict
        mydict = tagsdict.TagsDict(version);        
    elif output_format == "wordlist":
        import wordlistdict
        mydict = wordlistdict.WordListDict(version);        
    elif output_format == "check":
        import checkdict
        mydict = checkdict.checkDict(version);        
    else:
        import csvdict
        mydict = csvdict.CsvDict(version)
    return mydict
def main():
    args= grabargs()
    filename = args.filename
    limit = args.limit
    output_format =args.outformat
    version = args.version
    header = args.header    

    try:
        fl=open(filename, encoding='utf8');

    except:
        print(" Error :No such file or directory: %s" % filename)
        sys.exit(0)

    verb_field_number=2;
    verb_cat_field_number=3;

    line=fl.readline()
    text=u""
    verb_table=[];
    nb_field=12;
    mydict = None

    while line :
        line= line.strip('\n').strip()
        if not line.startswith("#"):
            liste=line.split("\t");
            if len(liste)>=nb_field:
                verb_table.append(liste);

        line=fl.readline();

    fl.close();
    # create header
    mydict = factory(output_format, version)
#    print mydict.add_header()
    if header:
        print(mydict.add_header())
    for tuple_verb in verb_table[:limit]:
        #~ verb_dict = decode_tuple_verb(tuple_verb);
        line = mydict.add_record(tuple_verb)
        if line:
            print(line)
    # create footer
    print(mydict.add_footer())

if __name__ == "__main__":
  main()







