# -*- coding=utf-8 -*-
#************************************************************************
# $Id: generatenoundict.py,v 0.8 2016/03/26 01:10:00 Taha Zerrouki $
#
# ------------
# Description: convert CSV files of nouns to suitable format
# ------------
#  Copyright (c) 2016,  Taha Zerrouki
#
#  This file is the main file to execute the application in the command line
#

#***********************************************************************/

import sys
import re
import string
import argparse
import os

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../support/'))
#~ import pyarabic.araby as araby
#~ import noundict_functions as ndf


scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
MAX_LINES_TREATED=1100000;
Separator="\t";

def grabargs():
    parser = argparse.ArgumentParser(description='Convert Noun dictionary to other format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-d", dest="outformat", nargs='?',
    help="output format(csv, sql, python, xml, check)", metavar="FORMAT")

    parser.add_argument("-v", dest="version", nargs='?',
    help="Release version", metavar="Version")
    
    parser.add_argument("-a",dest="all", type=bool, nargs='?',
                        const=True, 
                        help="Generate all stopwords forms")
    parser.add_argument("--header",dest="header", type=bool, nargs='?',
                        const=True, 
                        help="add header")
    parser.add_argument("-l",dest="limit", type=int, nargs='?',
                         help="the limit of treated lines")
    parser.add_argument("-t",dest="wordtype", type=str, nargs='?',
                        help="give the word type(fa3il,masdar, jamid, mochabaha,moubalagha,mansoub,)")
    args = parser.parse_args()
    return args                                                   


                 
def main():
    args= grabargs()
    filename = args.filename
    limit = args.limit
    output_format =args.outformat
    wordtype = args.wordtype
    version = args.version
    header = args.header
    #~ print "#--",filename,limit,display_format, wordtype;
    #exit();
    try:
        fl = open(filename, encoding="utf8");
    except:
        print(" Error :No such file or directory: %s" % filename)
        sys.exit(0)
    #~ print "#",filename,limit, output_format, wordtype, version
    #~ sys.exit()

    #display_format="txt"

    line = fl.readline()
    text = u""
    noun_table = [];
    nb_field = 2;
    while line :
        line = line.strip('\n')#.strip()
        if not line.startswith("#"):
            liste = line.split(Separator);
            if len(liste) >= nb_field:
                noun_table.append(liste);

        line = fl.readline()
    fl.close();

    #print "#", (u'\t'.join(field_id.keys())).encode('utf8');
    model = 0;
    if output_format == "sql":
        import sqldict
        mydict = sqldict.SqlDict(wordtype, version);
    elif output_format == "xml":
        import xmldict
        mydict = xmldict.XmlDict(wordtype, version);
    elif output_format == "stardict":
        import stardict
        mydict = stardict.StarDict(wordtype, version);
    elif output_format == "tags":
        import tagsdict
        mydict = tagsdict.TagsDict(wordtype, version);
    elif output_format == "spell":
        import spelldict
        mydict = spelldict.SpellDict(wordtype, version);
    elif output_format == "check":
        import checkdict
        mydict = checkdict.checkDict(version);        
    elif output_format == "taksir":
        import taksirdict
        mydict = taksirdict.TaksirDict(version);
    elif output_format == "wordlist":
        import wordlistdict
        mydict = wordlistdict.WordListDict(version);
    else:
        import csvdict
        mydict = csvdict.CsvDict(wordtype, version)    
    # create header
    #~ print(mydict)
    if header:
        print(mydict.add_header())
    for tuple_noun in noun_table[:limit]:
        l = mydict.add_record(tuple_noun)
        if l:
            print(l)
    # create footer
    f = mydict.add_footer()
    if f:
        print(f)
       
    
if __name__ == "__main__":
  main()
