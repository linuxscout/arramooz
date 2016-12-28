#!/usr/bin/python2
# -*- coding=utf-8 -*-
#************************************************************************
# $Id:generateverbdict.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#  Generate dictionary from manual dictionary
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
from libqutrub.ar_verb import *
from libqutrub.verb_db import *
from libqutrub.verb_valid import *

create_index_triverbtable();


scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
MAX_LINES_TREATED=1100000;

# trat the root, strip extra characters
def decode_root(root):
    root=root.replace(' ','')
    root=root.replace('[','')
    root=root.replace(']','')
    root=root.replace(araby.TATWEEL,'')
    return root;

#decode transitive
def decode_transitive(verb_cat):
    if verb_cat in ("P", "Ry", "Sx", "x", "y", "yw", "ywz","yy", "yz", "yzw"):
         return True;
    elif verb_cat in ( "Pu", "Su", "Sv",  "u", "v") :
        return False;
    else:
        return False;

#decode tense from the verb_cat
"""
لازم مطلق   u
    لا ينصرف مع المجهول ولا اﻷمر
لازم نسبي   v
    كل اﻷزمنة، وينصرف في المجهول مع المفرد الغائب فقط
متعدي غ ع   x
    ينصرف، أما في اﻹلحاق، فلا يتصل بضمائر المتكلم والمخاطب
متعدي ع y
    ينصرف ويلحق، ولا يتصل بضمائر المتكلم مع المتكلم
متعدي لمفعولين  yz
    ينصرف، ويلحق بالضمائر الواحدة والمتعددة
متعدي ع قلبي    yw
    ينصرف و يتصل مع الضمائر في كل حال
أمر فقط A
    ينصرف في الزمن الأمر فقط
ماضي فقط    P
    ينصرف في الزمن الأمر فقط
جامد    M
فعل لاشخصي  I
ماضي + مضارع    S
    ينصرف في الزمن المضارع والماضي فقط 
مبني للمجهول فقط    D
    ينصرف في الزمن المبني للمجهول فقط
مضارع + أمر R
    ينصرف في الزمن المضارع واﻷمر فقط 
"""
                                                         
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
    limit = MAX_LINES_TREATED;
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
    print "#",filename


    #print "len(TriVerbTable_INDEX={})", len(TriVerbTable_INDEX);


    #abbrevated=False;
    verb_field_number=2;
    root_field_number=1;
    verb_cat_field_number=3;

    line=fl.readline().decode("utf");
    text=u""
    verb_table=[];
    nb_field=2;
    while line :
        line = line.strip('\n')
        if not line.startswith("#"):
            liste=line.split("\t");
            if len(liste)>=nb_field:
                verb_table.append(liste);

        line=fl.readline().decode("utf8");
    fl.close();
    print "#total lines",len(verb_table)
    print "#", (u'\t'.join(["word","tri",'root',"future_type","transitive","nb_trans", "object_type", "reflexive_type", "tenses", "model","nb_case","verb_cat", "suggest"])).encode('utf8');
    model=0;
    cpt = 0
    for tuple_verb in verb_table[:limit]:
        word  = tuple_verb[verb_field_number].strip();
        root  = decode_root(tuple_verb[root_field_number].strip());
        model = tuple_verb[0].strip();

        if not is_valid_infinitive_verb(word):
            print (u"\t".join(["#", word, u"is invalid verb "] )).encode("utf8");
        else:
            #print word.encode("utf8")
            future_type = u"-";
            future_type = get_future_type_entree(future_type);
            verb_cat = tuple_verb[verb_cat_field_number].strip();
            # decode transitive flag
            #print "'%s'"%transitive;
            transitive=decode_transitive(verb_cat);
            #tenses=decode_tenses(verb_cat);
            # decode the tenses

            #init at False
            all=False;
            future=False;
            past=False;
            passive=False;
            imperative=False;
            confirmed=False;
            future_moode=False;
            # متعدي لغير العاقل
            unthink_trans=False;
            # متعدي للعاقل، تلقائيا اﻷفعال تقبل العاقل
            think_trans=True;
            #فعل قلوب
            reflexive_trans=False;
            #متعدي لمفعولين
            double_trans=False;
            if verb_cat =="A":# أمر فقط
                imperative=True;
            elif verb_cat =="D":# مبني للمجهول فقط
                passive=True;
            elif verb_cat =="I":#لاشخصي
                pass;
            elif verb_cat =="M":#جامد
                pass;
            elif    verb_cat =="P":# ماضي فقط
                past=True;
            elif    verb_cat =="Pu":# ماضي فقط لازم  مطلق
                past=True;
            elif    verb_cat =="Ry":# مضارع وأمر فقط
                future=True;
                imperative=True;
            elif    verb_cat =="Su":# ماضي ومضارع
                future=True;
                past=True;
                confirmed=True;
                future_moode=True;
            elif    verb_cat =="Sv":# ماضي ومضارع
                future=True;
                past=True;
                confirmed=True;
                future_moode=True;
            elif    verb_cat =="Sx":# ماضي ومضارع
                future=True;
                past=True;
                confirmed=True;
                future_moode=True;
            elif    verb_cat =="u":# لازم مطلق، لا مجهول ولا أمر
                future=True;
                past=True;
                confirmed=True;
                future_moode=True;
            elif    verb_cat =="v":# لازم نسبي، كل اﻷزمنة، لكن المجهول مع المفرد الغائب
                future=True;
                past=True;
                imperative=True;
                confirmed=True;
                future_moode=True;
                passive=False;
            elif    verb_cat in ("x","y", "yw", "ywz", "yy", "yz","yzw"): # ماضي فقط
                all=True;
                future=True;
                past=True;
                imperative=True;
                confirmed=True;
                future_moode=True;
                passive=False;
                if verb_cat in ("x","Sx"):
                    unthink_trans=True;
                elif verb_cat in ("yw", "ywz", "yy", "yz","yzw", "Ry"):
                    think_trans=True;
                    if verb_cat in ("ywz","yz","yzw"):
                        double_trans=True;
                    if verb_cat in ("ywz", "yw", "yzw"):
                        reflexive_trans=True;                                   
            else:
                all=True;
            nb_trans=0;
            object_type=u"----"
            reflexive_type=u"----";
            if transitive:
                transitive=u'متعد'
                nb_trans=1;
                if double_trans: 
                    nb_trans=2;
                if think_trans: 
                    object_type=u"عاقل";
                if unthink_trans: 
                    object_type=u"غيرع";
                if reflexive_trans: 
                    reflexive_type=u"فلبي";
            else: transitive=u'لازم'
        ##    codify the tense;
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
            #print transitive;

##          print ('\t'.join([word,future_type,str(transitive)])).encode('utf8');

            nb_case=0;
            suggest=u"";
            triliteral=u"غيرثل"
            if is_triliteral_verb(word):
                triliteral=u"ثلاثي"
        # search the future haraka for the triliteral verb
                liste_verb = find_alltriverb(word,FATHA,True);
        # if there are more verb forms, select the first one
                if  liste_verb:
                    word = liste_verb[0]["verb"]
                    haraka = liste_verb[0]["haraka"]
                    future_type = haraka;
                    transitive_mark = liste_verb[0]["transitive"].strip();
                    if transitive_mark in (u"م",u"ك"):
                        transitive = u"متعد"
                    else:
                        transitive = u"لازم"
                    if len(liste_verb)>1: 
                        #suggest=u"هل تقصد؟<br/>"
                        nb_case = len(liste_verb);
        # the other forms are suggested
                    for i in range(1,len(liste_verb)):
                        suggested_word = liste_verb[i]["verb"]
                        suggested_haraka = liste_verb[i]["haraka"]
                        suggested_transitive = liste_verb[i]["transitive"]
                        future_form = get_future_form(suggested_word,suggested_haraka);
                        suggest=u"\t".join([suggest,suggested_word,u"["+suggested_haraka+u"]"]);
                else:suggest="-"
            print (u'\t'.join([word,triliteral,root,future_type,transitive,str(nb_trans), object_type, reflexive_type, tenses, model,str(nb_case),verb_cat, suggest])).encode('utf8');
            
if __name__ == "__main__":
  main()







