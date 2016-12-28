#!/usr/bin/python2
# -*- coding=utf-8 -*-
#************************************************************************
# convert some numeric tags into letter tags
#
#***********************************************************************/



import sys,re,string
import sys, getopt, os
from spellverb import *
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
MAX_LINES_TREATED=1100000;

replacement={
"10":"Ta",
"20":"Tb",
"30":"Tc",
"40":"Td",
"50":"Te",
"60":"Tf",

"11":"Tg",
"21":"Th",
"31":"Ti",
"41":"Tj",
"51":"Tk",
"61":"Tl",

"12":"Tm",
"22":"Tn",
"32":"To",
"42":"Tp",
"52":"Tq",
"62":"Tr",

"13":"Ts",
"23":"Tt",
"33":"Tu",
"43":"Tv",
"53":"Tx",
"63":"Ty",

}
# trat the root, strip extra characters
def decode_root(root):
    root=root.replace(' ','')
    root=root.replace('[','')
    root=root.replace(']','')
    root=root.replace(TATWEEL,'')
    return root;


def usage():
# "Display usage options"
    print "(C) CopyLeft 2009, %s"%AuthorName
    print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
    print "\t[-h | --help]\t\toutputs this usage message"
    print "\t[-v | --version]\tprogram version"
    print "\t[-f | --file= filename]\tinput file to %s"%scriptname
    print "\t[-l | --limit= limit_ number]\tthe limit of treated lines %s"%scriptname
    print "\r\nN.B. FILE FORMAT is descripted in README"
    print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
    fname = ''
    limit = 0;
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:f:l:",
                               ["help", "version", "file=","limit="],)
    except getopt.GetoptError:
        usage()
        sys.exit(0)
    for o, val in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-v", "--version"):
            print scriptversion
            sys.exit(0)
        if o in ("-f", "--file"):
            fname = val
        if o in ("-l", "--limit"):
            try:
                limit = int(val);
            except:
                limit=MAX_LINES_TREATED;

            
    return fname,limit


                 
def main():
    filename,limit= grabargs()
    try:
        fl=open(filename);
    except:
        print " Error :No such file or directory: %s" % filename
        sys.exit(0)
    print "#",filename;


    line=fl.readline().decode("utf");
    text=u""
    tools_table=[];
    nb_field=2;
    while line :
        line=line.strip('\n')
        if not line.startswith("#"):
            liste=line.split("/");
            if len(liste)>=nb_field:
                word=liste[0];
                flag=liste[1];
                listflag=expand_flags(flag);
                newlist=[];
                for item in listflag:
                    if replacement.has_key(item):
                        newlist.append(replacement[item]);
                    else:
                        newlist.append(item);
                newlist=list(set(newlist))
                newlist.sort();
                #print u"\t".join([word, flag]).encode('utf8');
                print u"/".join([word, u"".join(newlist)]).encode('utf8');
                #print u",".join(listflag).encode('utf8');
                #print u",".join(newlist).encode('utf8');
                tools_table.append(liste);

        line=fl.readline().decode("utf8");
    fl.close();



if __name__ == "__main__":
  main()







