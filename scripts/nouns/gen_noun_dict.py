#!/usr/bin/python
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
import getopt
import os

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../support/'))
import pyarabic.araby as araby
import noundict_functions as ndf


scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
MAX_LINES_TREATED=1100000;
Separator="\t";

                                                         
def usage():
# "Display usage options"
    print "(C) CopyLeft 2016, %s"%AuthorName
    print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
    print "\t[-h | --help]\t\toutputs this usage message"
    print "\t[-v | --version= dataversion]\tset generated data version"
    print "\t[-f | --file= filename]\tinput file to %s"%scriptname
    print "\t[-d | --display= format]\tdisplay format (txt,sql, python, xml) %s"%scriptname
    print "\t[-t | --type= wordtype]\tgive the word type(fa3il,masdar, jamid, mochabaha,moubalagha,mansoub,) %s"%scriptname
    print "\t[-l | --limit= limit_ number]\tthe limit of treated lines %s"%scriptname
    print "\r\nN.B. FILE FORMAT is descripted in README"
    print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
    fname = ''
    limit = MAX_LINES_TREATED;
    wordtype="typo";
    display="txto"; 
    version = ""
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:v:f:d:t:l:",
                               ["help", "version=", "file=","display=","type=","limit=",],)
    except getopt.GetoptError:
        usage()
        sys.exit(0)
    for o, val in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-f", "--file"):
            fname = val
        if o in ("-v", "--version"):
            version = val
        if o in ("-l", "--limit"):
            try:
                limit = int(val);
            except:
                limit=MAX_LINES_TREATED;
        else:
            limit=MAX_LINES_TREATED;
        if o in ("-d", "--display"):
            display=val;
        if o in ("-t", "--type"):
            wordtype=val;
    #print fname,limit,display, wordtype;       
    return (fname,limit,display,wordtype, version);


                 
def main():
    filename,limit, output_format, wordtype, version= grabargs()
    #print "#--",filename,limit,display_format, wordtype;
    #exit();
    try:
        fl = open(filename);
    except:
        print " Error :No such file or directory: %s" % filename
        sys.exit(0)
    #print "#",filename

    #display_format="txt"

    line = fl.readline().decode("utf8");
    text = u""
    noun_table = [];
    nb_field = 2;
    while line :
        line = line.strip('\n')#.strip()
        if not line.startswith("#"):
            liste = line.split(Separator);
            if len(liste) >= nb_field:
                noun_table.append(liste);

        line = fl.readline().decode("utf8");
    fl.close();

    #print "#", (u'\t'.join(field_id.keys())).encode('utf8');
    model = 0;
    if output_format == "sql":
        mydict = ndf.SqlDict(wordtype, version);
    elif output_format == "xml":
        mydict = ndf.XmlDict(wordtype, version);
    else:
        mydict = ndf.CsvDict(wordtype, version)    
    # create header
    print mydict.add_header().encode('utf8')
    for tuple_noun in noun_table[:limit]:
        print mydict.add_record(tuple_noun).encode('utf8')
    # create footer
    print mydict.add_footer().encode('utf8')

if __name__ == "__main__":
  main()







