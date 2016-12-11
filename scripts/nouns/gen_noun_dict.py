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
from noundict_functions import *


scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
MAX_LINES_TREATED=1100000;
Separator="\t";

#decode tags from the noun attributes
"""
0   رقم
1   مشكول
2   جذر
3   وزن
4   صنف
5   أصل
6   جنس
7   مؤنث
8   مذكر
9   عدد
10  الجمع
11  مفرد
12  التأنيث
13  التثنية
14  ج. مؤ. س.
15  ج. مذ. س.
16  المنقوص
17  تنوين النصب
18  نسب
19  إض. لف.
20  ـو
21  ك
22  كال
23  ها
24  هم
25  تنوين النصب للجمع
26  شرح
"""
                                                         
def usage():
# "Display usage options"
    print "(C) CopyLeft 2016, %s"%AuthorName
    print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
    print "\t[-h | --help]\t\toutputs this usage message"
    print "\t[-v | --version]\tprogram version"
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
    if not sys.argv[1:]:
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:f:d:t:l:",
                               ["help", "version", "file=","display=","type=","limit=",],)
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
        else:
            limit=MAX_LINES_TREATED;
        if o in ("-d", "--display"):
            display=val;
        if o in ("-t", "--type"):
            wordtype=val;
    #print fname,limit,display, wordtype;       
    return (fname,limit,display,wordtype);


                 
def main():
    filename,limit,display_format, wordtype= grabargs()
    #print "#--",filename,limit,display_format, wordtype;
    #exit();
    try:
        fl = open(filename);
    except:
        print " Error :No such file or directory: %s" % filename
        sys.exit(0)
    #print "#",filename
    fields={};
    field_id={
        'id':0,                 #رقم    id
        'vocalized':1,          #جذر     root
        'unvocalized':2,       # غير مشكول
        'root':3,               #مشكول    vocalized
        'wazn':4,               #وزن    wazn
        'category':5,           #صنف    category
        'original':6,           #أصل    original
        'defined':7,
        'gender':8,             #جنس    gender
        'feminin':9,            #مؤنث    feminin
        'masculin':10,           #مذكر    masculin
        'number':11,             #عدد    number
        'plural':12,            #الجمع    plural
        'single':13,            #مفرد    single
        'feminable':14,         #التأنيث    does the word accept feminin
        'dualable':15,          #التثنية    does the word accept dual_form
        'feminin_plural':16,    #ج. مؤ. س.    does the word accept feminin_plural,
        'masculin_plural':17,   #ج. مذ. س.    does the word accept masculin_plural,
        'mankous':18,           #المنقوص    mankous
        'tanwin_nasb':19,       #تنوين النصب    Tanwin Nasb
        'relative':20,          #نسب    relative
        'annex':21,             #إضافة لفظية    oral annexation  
        'w_suffix':22,          #ـو    accept Waw suffix
        'k_suffix':23,          #ك    accept Kaf suffix
        'kal_prefix':24,        #كال    accept Kaf+Alef+Lam  preffix
        'ha_suffix':25,         #ها    accept Heh+Alef suffix
        'hm_suffix':26,         #هم    accept Heh+Meem suffix
        'plural_tanwin_nasb':27, #تنوين النصب للجمع    doew th plural form accept tawnin mansoub
        'definition':28,        #الشرح    Definition of the word
    }
    #give the display order for text format display
    display_order=[
            'id',
            'vocalized',
            'unvocalized',
            'normalized',
            'stamp',
            'wordtype',
            'root',
            'wazn',               #وزن    wazn
            'category',
            'original',
            'defined',          
            'gender',             #جنس    gender
            'feminin',            #مؤنث    feminin
            'masculin',           #مذكر    masculin
            'mankous',
            'feminable',
            'number',
            'single',
            'dualable',
            'masculin_plural',
            'feminin_plural',
            'broken_plural',
            'mamnou3_sarf',
            'relative',
            'w_suffix',
            'hm_suffix',
            'kal_prefix',
            'ha_suffix',
            'k_suffix',
            'annex',
            'definition',
            'note',
            ]
    wordtype_table={
        "fa3il":u"اسم فاعل",
        "masdar":u"مصدر",
        "jamid":u"جامد",
        "maf3oul":u"اسم مفعول",     
        "mouchabbaha":u"صفة مشبهة",
        "moubalagha":u"صيغة مبالغة",
        "mansoub":u"منسوب",
        "tafdil":u"اسم تفضيل",\
        "sifates":u"صفة",       
    }
    counter_table={
        "tafdil":      1,           #372
        "sifates":     500,         #522
        "mouchabbaha": 2000,     #785
        "mansoub":     3000,            #864
        "maf3oul":     4000,       #1261    
        "moubalagha":  6000,        #1941
        "fa3il":       8000,      # count of 4534
        "masdar":     15000,        #7345
        "jamid":      25000,        #10262

    }
    #display_format="txt"
    id = counter_table.get(wordtype, 1);
    wordtype = wordtype_table.get(wordtype, "");

    if not wordtype: print "Fatal Error : unsupported wordtype", wordtype;
        #exit();
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
    #print header 
    if display_format == "txt":
        print "#", u"\t".join(display_order).encode('utf8');
    elif display_format == "sql":
        #sqlite 
        print u"""CREATE TABLE  IF NOT EXISTS `nouns` (
          `id` int(11) unique,
          `vocalized` varchar(30) DEFAULT NULL,
          `unvocalized` varchar(30) DEFAULT NULL,
          `normalized` varchar(30) DEFAULT NULL,
          `stamp` varchar(30) DEFAULT NULL,
          `wordtype` varchar(30) DEFAULT NULL,
          `root` varchar(10) DEFAULT NULL,
          `wazn` varchar(30) DEFAULT NULL,
           `category` varchar(30) DEFAULT NULL,
          `original` varchar(30) DEFAULT NULL,
          `defined` varchar(30) DEFAULT NULL,
          `gender` varchar(30) DEFAULT NULL,
          `feminin` varchar(30) DEFAULT NULL,
          `masculin` varchar(30) DEFAULT NULL,
          `mankous` varchar(30) DEFAULT NULL,
          `feminable` varchar(30) DEFAULT NULL,
          `number` varchar(30) DEFAULT NULL,
          `single` varchar(30) DEFAULT NULL,
          `dualable` varchar(30) DEFAULT NULL,
          `masculin_plural` varchar(30) DEFAULT NULL,
          `feminin_plural` varchar(30) DEFAULT NULL,
          `broken_plural` varchar(30) DEFAULT NULL,
          `mamnou3_sarf` varchar(30) DEFAULT NULL,
          `relative` varchar(30) DEFAULT NULL,
          `w_suffix` varchar(30) DEFAULT NULL,
          `hm_suffix` varchar(30) DEFAULT NULL,
          `kal_prefix` varchar(30) DEFAULT NULL,
          `ha_suffix` varchar(30) DEFAULT NULL,
          `k_suffix` varchar(30) DEFAULT NULL,
          `annex` varchar(30) DEFAULT NULL,
          `definition` text,
          `note` text
        ) ;""".encode('utf8')
        mysql = u"""CREATE TABLE  IF NOT EXISTS `nouns` (
          `id` int(11) unique auto_increment,
          `vocalized` varchar(30) DEFAULT NULL,
          `unvocalized` varchar(30) DEFAULT NULL,
          `wordtype` varchar(30) DEFAULT NULL,
          `root` varchar(30) DEFAULT NULL,
          `original` varchar(30) DEFAULT NULL,
          `mankous` varchar(30) DEFAULT NULL,
          `feminable` varchar(30) DEFAULT NULL,
          `number` varchar(30) DEFAULT NULL,
          `dualable` varchar(30) DEFAULT NULL,
          `masculin_plural` varchar(30) DEFAULT NULL,
          `feminin_plural` varchar(30) DEFAULT NULL,
          `broken_plural` varchar(30) DEFAULT NULL,
          `mamnou3_sarf` varchar(30) DEFAULT NULL,
          `relative` varchar(30) DEFAULT NULL,
          `w_suffix` varchar(30) DEFAULT NULL,
          `hm_suffix` varchar(30) DEFAULT NULL,
          `kal_prefix` varchar(30) DEFAULT NULL,
          `ha_suffix` varchar(30) DEFAULT NULL,
          `k_suffix` varchar(30) DEFAULT NULL,
          `annex` varchar(30) DEFAULT NULL,
          `definition` text,
          `note` text
        )  DEFAULT CHARSET=utf8;""".encode('utf8')
    elif display_format == "xml": 
        print "<?xml version='1.0' encoding='utf-8'?>\n<dictionary>";
    elif display_format == "python": 
        print """#!/usr/bin/python
# -*- coding=utf-8 -*-
NOUN_DICTIONARY={"""

    for tuple_noun in noun_table[:limit]:
        #extract field from the noun tuple
        fields={};
        for key in field_id.keys():
            try:
                fields[key] = tuple_noun[field_id[key]].strip();
            except IndexError:
                print "#"*5, "key error [%s],"%key, field_id[key], len(tuple_noun);
                print tuple_noun
                sys.exit()
        # treat specific fields
        fields['note']="";
        # word root
        #fields['root']  =  fields['root'];
        #if fields['root'] == "":
        if fields['number'] == u"جمع":
            fields['number'] == u"جمع تكسير"
            #fields['note']   = u":".join([fields['note'],u"لا جذر", u"لا مفرد"]);          
        else:
            fields['number'] = u"مفرد"
        # make note  if definition is not given
        if not fields['definition']:
            fields['note'] = u":".join([fields['note'],u"لا شرح"]);

        #الممنوع من الصرف
        if fields['tanwin_nasb']=="":
            fields['mamnou3_sarf']=u"ممنوع من الصرف";
        else:
            fields['mamnou3_sarf']=u"";
        # get the vocalized form 
        #fields['vocalized']      = decode_vocalized(fields['vocalized']);
        fields['unvocalized'] = araby.strip_tashkeel(fields['vocalized']);
        # word type, must be defined for every file         
        fields['wordtype']   = wordtype;
        # create mankous form if exist
        #if fields['mankous'] == "Tk":
        #   fields['mankous_from'] = get_mankous(fields['vocalized']);  
        # create feminin form if is possibel
        #if fields['feminable'] == "Ta":
        #   fields['feminin_from'] = get_feminin(fields['vocalized']);  
        # extarct broken plurals
        if fields['plural']:
            fields['broken_plural'] = fields['plural']; 
        else:
            fields['broken_plural'] = "";
        #display order
        fields['normalized'] = araby.normalize_hamza(fields['unvocalized'])
        fields['stamp'] = word_stamp(fields['unvocalized'])
        if display_format == "txt":
            items=[];
            for k in range(len(display_order)):
                key=display_order[k];
                items.append(fields[key]);
                line=u"\t".join(items);
        elif display_format=="sql": 
            # to reduce the sql file size, 
            # doesn't work with multiple files
            #items=["'%d'"%id,];
            #line="insert into nouns values "   #%", ".join(display_order);
            line="insert into nouns (%s) values "%", ".join(display_order);
            fields['id'] = id
            items=[];           
            for k in range(len(display_order)):
                key=display_order[k];
                if key == "id":
                    items.append(u"%d"%fields[key]);
                else:
                    items.append(u"'%s'"%fields[key]);

            line+=u"(%s);"%u",".join(items);
        elif display_format=="xml": 
            line="<noun id='%d'>"%id;
            for k in range(len(display_order)):
                key=display_order[k];
                if display_order[k] != "id":
                    line+=u"<%s>%s</%s> "%(key,fields[key],key);
            line+=u"</noun>";
        elif display_format=="python": 
            line="u'%s':{"%fields['vocalized'];
            for k in range(len(display_order)):
                key=display_order[k];
                line+=u"u'%s':u'%s', "%(key,fields[key]);
            line+=u"},";
        
        else: line="unsupported format";
        print line.encode('utf8');
        #increment ID
        id+=1;
    # end tags
    
    if display_format=="xml": 
        print "</dictionary>";
    if display_format=="python": 
        print "};";
if __name__ == "__main__":
  main()







