#!/usr/bin/python
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
import getopt
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

def yes(bool):
    if bool: return "y";
    else: return "n";

def usage():
# "Display usage options"
    print "(C) CopyLeft 2009, %s"%AuthorName
    print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
    print "\t[-h | --help]\t\toutputs this usage message"
    print "\t[-v | --version]\tprogram version"
    print "\t[-f | --file= filename]\tinput file to %s"%scriptname
    print "\t[-o | --output= format]\toutput file format %s"%scriptname
    print "\t[-l | --limit= limit_ number]\tthe limit of treated lines %s"%scriptname
    print "\r\nN.B. FILE FORMAT is descripted in README"
    print "\r\nThis program is licensed under the GPL License\n"


def grabargs():
#  "Grab command-line arguments"
    fname = ''
    limit=MAX_LINES_TREATED;
    output = "csv"
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:f:l:o:",
                               ["help", "version", "file=","limit=", "output="],)
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
        if o in ("-o", "--output"):
            output = val.lower()
        if o in ("-f", "--file"):
            fname = val
        if o in ("-l", "--limit"):
            try:
                limit = int(val);
            except:
                limit=MAX_LINES_TREATED;

            
    return fname,limit, output


                 
def main():
    filename,limit, output_format= grabargs()
    try:
        fl=open(filename);
    except:
        print " Error :No such file or directory: %s" % filename
        sys.exit(0)

    verb_field_number=2;
    verb_cat_field_number=3;

    line=fl.readline().decode("utf");
    text=u""
    verb_table=[];
    nb_field=12;
    while line :
        line= line.strip('\n').strip()
        if not line.startswith("#"):
            liste=line.split("\t");
            if len(liste)>=nb_field:
                verb_table.append(liste);

        line=fl.readline().decode("utf8");
    fl.close();
    if output_format=="xml":
        print "<?xml version='1.0' encoding='utf8'?>\n<dictionary>";
    elif output_format=="sql":
        print u"""create table verbs
    (
    id int unique auto_increment,
    vocalized varchar(30) not null,
    unvocalized varchar(30) not null,
    root varchar(30),
    future_type varchar(5),
    triliteral  ENUM( "n", "y" ) NOT NULL default "y", 
    transitive  ENUM( "n", "y" ) NOT NULL default "y", 
    double_trans  ENUM( "n", "y" ) NOT NULL default "y", 
    think_trans  ENUM( "n", "y" ) NOT NULL default "y", 
    unthink_trans  ENUM( "n", "y" ) NOT NULL default "y", 
    reflexive_trans  ENUM( "n", "y" ) NOT NULL default "y", 
    past  ENUM( "n", "y" ) NOT NULL default "y", 
    future  ENUM( "n", "y" ) NOT NULL default "y",  
    imperative  ENUM( "n", "y" ) NOT NULL default "y", 
    passive  ENUM( "n", "y" ) NOT NULL default "y",  
    future_moode  ENUM( "n", "y" ) NOT NULL default "y", 
    confirmed  ENUM( "n", "y" ) NOT NULL default "y", 
    PRIMARY KEY (id)
    )"""
    else : #output_format will be csv: 
        line = u"\t".join(["id", "word", "unvocalized" , "root" , "future_type" ,"triliteral"  , "transitive"  , "double_trans"  , "think_trans"  , "unthink_trans"  , "reflexive_trans"  , "past"  , "future"  ,  "imperative"  ," passive"  , " future_moode"  , "confirmed"])
        print line.encode('utf8');         
    id=10;
    for tuple_verb in verb_table[:limit]:
        id+=1;
    # word  tri root    future_type transitive  nb_trans    object_type reflexive_type  tenses  model   nb_case verb_cat    suggest
        word=tuple_verb[0].strip();
        unvocalized = araby.strip_tashkeel(word);
        tri=tuple_verb[1].strip();
        root=tuple_verb[2].strip();
        future_type=tuple_verb[3].strip();
        transitive=tuple_verb[4].strip();
        nb_trans=tuple_verb[5].strip();
        object_type=tuple_verb[6].strip();
        reflexive_type=tuple_verb[7].strip();
        tenses=tuple_verb[8].strip();
        #model=tuple_verb[9].strip();
        nb_case=tuple_verb[10].strip();
        #verb_cat=tuple_verb[11].strip();
        #suggest=tuple_verb[12].strip();

        # Adopt fields to the actual program
        #word;
        if tri==u"ثلاثي":
            triliteral=True;
        else:
            triliteral=False;
        #root
        #future_type
        if transitive!=u"متعد":
            transitive=False;
            unthink_trans=False;    # متعدي لغير العاقل
            think_trans=False;          # متعدي للعاقل، تلقائيا اﻷفعال تقبل العاقل
            reflexive_trans=False;    #فعل قلوب
            double_trans=False;             #متعدي لمفعولين
        else:
            transitive=True;
            ## 
            if nb_trans=="2":
                double_trans=True;
            else:
                double_trans=False;
            # TYPE OF THE OBJECT, REASONALBEL, OR NOT
            if object_type==u"عاقل":
                think_trans=True;
                unthink_trans=False;
            elif object_type==u"غيرع":
                think_trans=False;
                unthink_trans=True;
            else:
                think_trans=False;
                unthink_trans=False;
            # reflexive object  فعل القلوب المتعدي، أظنني   
        if reflexive_type==u"قلبي":
            reflexive_trans=True;
        else:
            reflexive_trans=False;
        # decode tenses
        all, past, future, passive, imperative, future_moode, confirmed = vdf.decode_tenses(tenses);
        if all:
            tenses=u"يعملان";
        else:
            tenses=u"";
            if past: tenses+=u"ي";
            else: tenses+="-";
            if future: tenses+=u"ع";
            else: tenses+="-";
            if imperative: tenses+=u"م";
            else: tenses+="-";
            if passive: tenses+=u"ل";
            else: tenses+=u"-";
            if future_moode: tenses+=u"ا";
            else: tenses+=u"-";
            if confirmed: tenses+=u"ن";
            else: tenses+=u"-";
        # print for verify the line

        if output_format=="xml": 
            print "<verb ",
            #print (u"\t".join(tuple_verb)).encode('utf8');
            print  (u"future_type='%s' "%future_type).encode('utf8'),
            print  (u"triliteral='%s'"%str(triliteral)).encode('utf8'),
            print  (u"transitive='%s'"%str(transitive)).encode('utf8'),
            print  (u"double_trans='%s'"%str(double_trans)).encode('utf8'),
            print  (u"think_trans='%s'"%str(think_trans)).encode('utf8'),
            print  (u"unthink_trans='%s'"%str(unthink_trans)).encode('utf8'),
            print  (u"reflexive_trans='%s'"%str(reflexive_trans)).encode('utf8'),
            print  u">".encode('utf8');
            print  (u"<word>%s</word>"%word).encode('utf8');
            print  (u"<unvocalized>%s</unvocalized>"%unvocalized).encode('utf8');
            print  (u"<root>%s</root>"%root).encode('utf8');
            #print  (u"<tenses>%s</tenses>"%tenses).encode('utf8');
            print (u"<tenses past='%s' future='%s' imperative='%s' passive='%s' future_moode='%s' confirmed='%s'/>"%(str(past), str( future), str( imperative), str( passive), str( future_moode), str( confirmed))).encode('utf8');            
            print "</verb>";
        elif output_format=="sql": 
            #(vocalized, unvocalized, root, future_type, triliteral, transitive, double_trans, think_trans, unthink_trans, reflexive_trans, past, future, imperative, passive, future_moode, confirmed)
            line=u"insert into verbs ";
            line+="values ('%d','%s','%s','%s', '%s', '%s', '%s','%s','%s','%s', '%s', '%s', '%s','%s','%s','%s', '%s');"%(id, word, unvocalized , root , future_type ,yes(triliteral)  , yes(transitive)  , yes(double_trans)  , yes(think_trans)  , yes(unthink_trans)  , yes(reflexive_trans)  , yes(past)  , yes(future)  ,  yes(imperative)  ,yes( passive)  , yes( future_moode)  , yes(confirmed))
            print line.encode('utf8'); 
        else : #output_format will be csv: 
            line = u"\t".join([str(id), word, unvocalized , root , future_type ,yes(triliteral)  , yes(transitive)  , yes(double_trans)  , yes(think_trans)  , yes(unthink_trans)  , yes(reflexive_trans)  , yes(past)  , yes(future)  ,  yes(imperative)  ,yes( passive)  , yes( future_moode)  , yes(confirmed)])
            print line.encode('utf8'); 


    if output_format=="xml":print "</dictionary>";     
if __name__ == "__main__":
  main()







