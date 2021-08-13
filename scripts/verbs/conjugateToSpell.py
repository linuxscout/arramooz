#!/usr/bin/python2
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

##from verb_const import *
##from ar_ctype import *
##from classverb import *
from libqutrub.mosaref_main import *
import sys,re,string
import sys, getopt, os
from  spellverbconst import *
from  spellverb import *
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"

# Limit of the fields treatment

MAX_LINES_TREATED=1100000;



def usage():
# "Display usage options"
    print("(C) CopyLeft 2009, %s"%AuthorName)
    print("Usage: %s -f filename [OPTIONS]" % scriptname)
#"Display usage options"
    print("\t[-h | --help]\t\toutputs this usage message")
    print("\t[-v | --version]\tprogram version")
    print("\t[-f | --file= filename]\tinput file to %s"%scriptname)
    print("\t[-l | --limit= limit_ number]\tthe limit of treated lines %s"%scriptname)
    print("\r\nN.B. FILE FORMAT is descripted in README")
    print("\r\nThis program is licensed under the GPL License\n")


def grabargs():
#  "Grab command-line arguments"
    fname = ''
    limit=MAX_LINES_TREATED;
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
            print(scriptversion)
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
        print(" Error :No such file or directory: %s" % filename)
        sys.exit(0)



    #abbrevated=False;
    verb_field_number=2;
    verb_cat_field_number=3;

    line=fl.readline().decode("utf");
    text=u""
    verb_table=[];
    nb_field=12;
    while line :
        line = line.strip('\n')
        if not line.startswith("#"):
            liste=line.split("\t");
            if len(liste)>=nb_field:
                verb_table.append(liste);

        line=fl.readline().decode("utf8");
    fl.close();
    #limit=MAX_LINES_TREATED;
    for tuple_verb in verb_table[:limit]:
    # word  tri root    future_type transitive  nb_trans    object_type reflexive_type  tenses  model   nb_case verb_cat    suggest
        word=tuple_verb[0].strip();
        tri=tuple_verb[1].strip();
        #root=tuple_verb[2].strip();
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
        all, past, future, passive, imperative, future_moode, confirmed=decode_tenses(tenses);

        # print for verify the line
        VERIFY_INPUT=False;
        if VERIFY_INPUT: 
            print( "------------------------------");
            print(u"\t".join(tuple_verb));

            print(u"\t".join(['word',word,tuple_verb[0]]));
            print(u"\t".join(['future_type',future_type,tuple_verb[3]]));
            print(u"\t".join(['transitive',str(transitive),tuple_verb[4]]));
            print(u"\t".join(['double_trans',str(double_trans),tuple_verb[5]]));
            print(u"\t".join(['think_trans',str(think_trans),tuple_verb[6]]));
            print(u"\t".join(['unthink_trans',str(unthink_trans),tuple_verb[6]]));
            print(u"\t".join(['reflexive_trans',str(reflexive_trans),tuple_verb[7]]));
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
            print(u"\t".join(['tense',tenses,tuple_verb[8]]))
            print("------------------------------");

        # conjugate the verb with speling tags
        if not is_valid_infinitive_verb(word):
            print(u"#\t\tis invalid verb ",word)
        else:
            future_type=get_future_type_entree(future_type);
            conjugTable=do_sarf(word,future_type, all, past, future, passive, imperative, future_moode, confirmed, transitive, "DICT");
            TableEntries={}
            if conjugTable: 
                TableEntries={}

                for tense in conjugTable.keys():
                    for pronoun in conjugTable[tense].keys():
                        if pronoun!=PronounAntuma_f: 

                            flags=TabPrefixes[tense]['full'];
                    

                            # the passive tenses dont take object suffix, only with double transitie verbs
                            if (transitive and tense in TableIndicativeTense) or double_trans:#:
                                # add flags for suffixes
                                if think_trans and reflexive_trans: 
                                    flags+=TabSuffixesPronominale[pronoun]['full'];
                                else:
                                    flags+=TabSuffixes[pronoun]['full'];
                                #   add flag yeh for the الأفعال الخمسة 
                                if tense==TenseFuture and pronoun in (PronounAnti , PronounAntuma , PronounAntuma_f, PronounAntum    ,PronounHuma ,PronounHuma_f, PronounHum ):
                                    flags+=u"Ha";                                   
                            # add double object suffixe, if the verb is double transitive, and the tense is indicative 
                            if double_trans and tense in TableIndicativeTense:
                                # add flags for suffixes (double object)
                                    flags+=TabDisplayTagDouble[pronoun]['full'];
                            #add an entree to the table entrie
                            # this allows to reduce many cases into one entree
                            word_nm=ar_strip_marks(conjugTable[tense][pronoun]);
                            if TableEntries.has_key(word_nm):
                                TableEntries[word_nm]+=flags;
                            else:
                                TableEntries[word_nm]=flags;
                            #print (u'%s/%s\t%s%s'%(ar_strip_marks(conjugTable[tense][pronoun]), flags, word,verb_cat));
                # print element from the TableEntries
                for key in TableEntries.keys():
                    if key!="":
                        print(u'%s/%s'%(key,unify_flags(TableEntries[key])))               

if __name__ == "__main__":
  main()







