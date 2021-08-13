# -*- coding=utf-8 -*-
#************************************************************************
# $Id:generateverbdict.py,v 0.7 2009/06/02 01:10:00 Taha Zerrouki $
#  Generate dictionary from manual dictionary
#
#***********************************************************************/

import sys
import re
import string
import argparse
import os

#~ sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../support/'))
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr
from libqutrub.mosaref_main import get_future_form
from libqutrub.ar_verb import get_future_type_entree, is_triliteral_verb
#~ from libqutrub.verb_db import create_index_triverbtable, find_alltriverb
from libqutrub.verb_valid import is_valid_infinitive_verb

import triverbtable # local version

scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
MAX_LINES_TREATED=1100000;

def grabargs():
    parser = argparse.ArgumentParser(description='Convert Noun dictionary to other format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    parser.add_argument("-t", dest="triverbfilename", required=True,
    help="input file to convert which contain triverbs information", metavar="TRI verb FILE")
    
    parser.add_argument("-v", dest="version", nargs='?',
    help="Release version", metavar="Version")

    parser.add_argument("-l",dest="limit", type=int, nargs='?',
                         help="the limit of treated lines")

    args = parser.parse_args()
    return args
class verb_reader:
    def __init__(self, ):
        self.tritable = {}
        pass
    def run(self, command, verb_table, limit):
        if command =="test":
            print('test')
        elif command =="ayaspell":
            self.treat_verb_table(verb_table, limit)
        elif command =="sarf":
            self.treat_triverb(verb_table, limit)
        else:
            print("%s is Runing..."%command)
    # trat the root, strip extra characters
    @staticmethod
    def decode_root(root):
        root=root.replace(' ','')
        root=root.replace('[','')
        root=root.replace(']','')
        root=root.replace(araby.TATWEEL,'')
        return root;

    #decode transitive
    @staticmethod
    def decode_transitive(verb_cat):
        if verb_cat in ("P", "Ry", "Sx", "x", "y", "yw", "ywz","yy", "yz", "yzw"):
            return True;
        elif verb_cat in ( "Pu", "Su", "Sv",  "u", "v") :
            return False;
        # used to handle sarf data base ك مشترك، ل لازم، ميم متعدي
        elif verb_cat in (araby.MEEM, araby.KAF):
            return True
        elif verb_cat in (araby.LAM,):
            return False
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
                                                             



    def decode_verb_tuple(self, tuple_verb):
        """
        """
        #abbrevated=False;
        verb_field_number=2;
        root_field_number=1;
        verb_cat_field_number=3;
        root  = self.decode_root(tuple_verb[root_field_number].strip());        
        word  = tuple_verb[verb_field_number].strip();


        if not is_valid_infinitive_verb(word):
            return {"text":u"#\t'%s'\tis invalid verb "%word};
        else:

            model = tuple_verb[0].strip();            
            #print word.encode("utf8")
            future_type = u"-";
            future_type = araby.name(get_future_type_entree(future_type));
            verb_cat = tuple_verb[verb_cat_field_number].strip();
            # decode transitive flag
            #print "'%s'"%transitive;
            transitive = self.decode_transitive(verb_cat);
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
            else: 
                transitive=u'لازم'
        ##    codify the tense;
            tenses = self.encode_tense(all, past, future, imperative, passive, future_moode, confirmed)

    ##          print ('\t'.join([word,future_type,str(transitive)]));

            nb_case=0;
            suggest=u"";
            triliteral=u"غيرثل"
            if is_triliteral_verb(word):
                triliteral=u"ثلاثي"
            if False:
        # search the future haraka for the triliteral verb
                liste_verb = find_alltriverb(word, araby.FATHA,True);
        # if there are more verb forms, select the first one
                filtered = [item for item in liste_verb if item['verb'] == word]
                if filtered:
                    #~ word = liste_verb[0]["verb"]
                    haraka = filtered[0]["haraka"]
                    future_type = haraka;
                    transitive_mark = filtered[0]["transitive"].strip();
                    if transitive_mark in (u"م",u"ك"):
                        transitive = u"متعد"
                    else:
                        transitive = u"لازم"
                else:
                    return {"text":u"#gen_verb_dict: %s error no tri verb"%word}
                if  liste_verb:                        
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
            verb_dict = {'nb_case': str(nb_case), 
                 'word': word, 
                 'tenses': tenses, 
                 'nb_trans': nb_trans, 
                 'suggest': suggest, 
                 'triliteral': triliteral, 
                 'object_type': object_type, 
                 'verb_cat': verb_cat, 
                 'future_type': future_type, 
                 'model': model, 
                 'transitive': transitive, 
                 'root': root, 
                 'reflexive_type': reflexive_type, 
                 }
            return verb_dict
            #~ return u'\t'.join([word,triliteral,root,future_type,transitive,str(nb_trans), object_type, reflexive_type, tenses, model,str(nb_case),verb_cat, suggest])

    def  encode_tense(self, all, past, future, imperative, passive, future_moode, confirmed):
        """ encode tenses """
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
        return tenses

    def treat_verb_table2(self, verb_table, limit):
        """ readlines and treat them"""

        print("total lines",len(verb_table))
        print("#", (u'\t'.join(["word","tri",'root',"future_type","transitive","nb_trans", "object_type", "reflexive_type", "tenses", "model","nb_case","verb_cat", "suggest"])));

        model=0;
        cpt = 0
        for tuple_verb in verb_table[:limit]:
            result = self.decode_verb_tuple(tuple_verb)
            print(result)

    def treat_verb_table(self, verb_table, limit):
        """ readlines and treat them"""
        tritable = {}
        # duplicated verbs to be checked
        check_verbs = []
        print("#total lines",len(verb_table))

        print("#", (u'\t'.join(["word","tri",'root',"future_type","transitive","nb_trans", "object_type", "reflexive_type", "tenses", "model","nb_case","verb_cat", "suggest"])));

        model=0;
        cpt = 0
        for tuple_verb in verb_table[:limit]:
            result = ""
            result_dict = self.decode_verb_tuple(tuple_verb)
            if result_dict.get("triliteral",'') != u"ثلاثي":
                result = self.print_tuple(result_dict)
                print(result)
            else:
                # save the triverb to be used with triverb file                
                verb = result_dict.get('word','')
                if verb:
                    if verb in tritable:
                        tritable[verb].append(result_dict)
                        # print to check
                        if verb not in check_verbs:
                            check_verbs.append(verb)
                    else:
                        tritable[verb] = [result_dict, ]

        # print checked verbs 
        #~ for v in check_verbs:
            #~ for item in tritable[v]:
                #~ print "***check****", self.print_tuple(item)
        self.tritable = tritable
        return tritable
    def print_tuple(self, vdict):
        """
        convert tuple to string
        """
        if type(vdict) is list:
            print(arepr(vdict))
        if "text" in vdict:
            return vdict['text']
        else:
            return u'\t'.join([
            vdict["word"],
            vdict["triliteral"],
            vdict["root"],
            vdict["future_type"],
            vdict["transitive"],
            str(vdict["nb_trans"]),
            vdict["object_type"],
            vdict["reflexive_type"],
            vdict["tenses"],
            vdict["model"],
            str(vdict["nb_case"]),
            vdict["verb_cat"],
            vdict["suggest"]])
    def decode_triverb(self, verb_table, limit):
        """ readlines from files """
        verb_list = []
        for fields in verb_table:
            if len(fields)  >= 4:
                                    #الفعل  الجذر   باب التصريف T   id
                vdict= {"verb": fields[0],
                "root":fields[1],
                "haraka":araby.name(get_future_type_entree(fields[2])),
                "transitive":fields[3],
                }
                verb_list.append(vdict)
        return verb_list
    def treat_triverb(self, verb_table, limit):
        """ readlines and treat them"""
        # the key is the verb + conjugation class ( باب التصريف)
        verb_list = self.decode_triverb(verb_table, limit)
        #~ print("len(verb_list)",len(verb_list))
        #~ print(arepr(verb_list[:10]))
        table = triverbtable.TriVerbTable
        #~ for verb_key in table:
        for vdict in verb_list:
            #~ verb = verb_key[:-1]
            #~ transitive = self.decode_transitive(table[verb_key]['transitive'])
            #~ root = table[verb_key]['root']
            verb = vdict['verb']
            transitive = self.decode_transitive(vdict['transitive'])
            root = vdict['root']
            # fields to get from ayaspell
            model = ""
            verb_cat = ""
            object_type =""
            nb_trans =""
            reflexive_type =""
            tenses =""
            transitive = u"متعد" if transitive else u"لازم"

            if verb in self.tritable:
                # a list of verbs
                accepted_list = [vd for vd in self.tritable[verb] 
                        if vd['root']==root and vd['transitive']==transitive]
                for verb_variant in accepted_list:
                    model = verb_variant["model"]
                    verb_cat = verb_variant["verb_cat"]
                    object_type =verb_variant["object_type"]
                    nb_trans =verb_variant["nb_trans"]
                    reflexive_type =verb_variant["reflexive_type"]
                    tenses = verb_variant["tenses"]
                    verb_dict = {'nb_case': 0,#str(nb_case), 
                         'word': verb, 
                         'tenses': tenses, 
                         'nb_trans': nb_trans, 
                         'suggest': "", 
                         'triliteral': u"ثلاثي", 
                         'object_type': object_type, 
                         'verb_cat': verb_cat, 
                         'future_type': vdict['haraka'], 
                         'model': model, 
                         'transitive':transitive, 
                         'root': vdict['root'], 
                         'reflexive_type': reflexive_type, 
                         }
                    #~ print "***TRI****", self.print_tuple(verb_dict)
                    print(self.print_tuple(verb_dict))

            else:
                model       = "NA"
                verb_cat    = "NA"
                object_type = "NA"
                nb_trans = 1 if transitive == u"متعد" else 0
                reflexive_type = "NA"
                tenses = u"يعملان"

                verb_dict = {'nb_case': 0,#str(nb_case), 
                     'word': verb, 
                     'tenses': tenses, 
                     'nb_trans': nb_trans, 
                     'suggest': "", 
                     'triliteral': u"ثلاثي", 
                     'object_type': object_type, 
                     'verb_cat': verb_cat, 
                     'future_type': vdict['haraka'], 
                     'model': model, 
                     'transitive':transitive, 
                     'root': vdict['root'], 
                     'reflexive_type': reflexive_type, 
                     }
                #~ print "***TRI*NA****", self.print_tuple(verb_dict)
                print(self.print_tuple(verb_dict))

    def read_file(self, fl):
        """ read lines as lists from file"""
        line=fl.readline()
        text=u""
        verb_table=[];
        nb_field=2;
        while line :
            line = line.strip('\n')
            if not line.startswith("#"):
                liste=line.split("\t");
                if len(liste)>=nb_field:
                    verb_table.append(liste);

            line=fl.readline()
        fl.close();
        return verb_table

        

TRIVERBTABLE_INDEX = {}
def create_index_triverbtable():
    """ Create index from the verb dictionary
    to accelerate the search in the dictionary for verbs
    @return: create the TRIVERBTABLE_INDEX
    @rtype: None
    """
    # the key is the vocverb + the bab number
    for key in triverbtable.TriVerbTable.keys():
        vocverb = triverbtable.TriVerbTable[key]['verb']
        unvverb = araby.strip_harakat(vocverb)
        normverb = araby.normalize_hamza(unvverb)
        if normverb in TRIVERBTABLE_INDEX:
            TRIVERBTABLE_INDEX[normverb].append(key)
        else:
            TRIVERBTABLE_INDEX[normverb] = [key, ]

def find_alltriverb(triverb, givenharaka = araby.FATHA, 
vocalised_entree = False):
    """
    Find the triliteral verb in the dictionary (TriVerbTable)
    return a list of possible verb forms
    each item contains:
        - 'root':
        - 'haraka:
        - 'bab':
        - 'transitive':
    @param triverb: given verb.
    @type triverb: unicode.
    @param givenharaka: given haraka of tuture type of the verb, 
    default(FATHA).
    @type givenharaka: unicode.
    @param VocalisedEntree: True if the given verb is vocalized, 
    default False.
    @type VocalisedEntree: Boolean.
    @return: list of triliteral verbs.
    @rtype: list of dicts.
    """
    liste = []
    if vocalised_entree:
        verb_nm = araby.strip_harakat(triverb)
    else:
        verb_nm = triverb

    normalized = araby.normalize_hamza(verb_nm)
    if normalized in TRIVERBTABLE_INDEX:
        for verb_voc_id in TRIVERBTABLE_INDEX[normalized]:
            if triverb == triverbtable.TriVerbTable[verb_voc_id]['verb'] and \
             givenharaka == triverbtable.TriVerbTable[verb_voc_id]['haraka']:
                liste.insert(0, triverbtable.TriVerbTable[verb_voc_id])
#            if VocalisedEntree:
                #if verb_voc_id[:-1] == triverb:
                #    liste.append(TriVerbTable[verb_voc_id])
            else:
                liste.append(triverbtable.TriVerbTable[verb_voc_id])
    else:
        print("triverb has no verb")
    return liste            

def main():
    args = grabargs()

    filename = args.filename
    filename_3verb = args.triverbfilename
    limit= args.limit
    try:
        fl=open(filename);
    except:
        print(" Error :No such file or directory: %s" % filename)
        sys.exit(0)
    print("#",filename)

    try:
        fl3=open(filename_3verb);
    except:
        print(" Error :No such file or directory: %s" % filename_3verb)
        sys.exit(0)
    print("#",filename_3verb)

    create_index_triverbtable();
    #print "len(TriVerbTable_INDEX={})", len(TriVerbTable_INDEX);

    # FIRST FILE

    reader = verb_reader()
    verb_table = reader.read_file(fl)
    verb_table3 = reader.read_file(fl3)
    command = "ayaspell"
    reader.run(command, verb_table, limit)
    command = "sarf"
    reader.run(command, verb_table3, limit)
    #~ print("len(triverbtable.TriVerbTable)",len(triverbtable.TriVerbTable))
if __name__ == "__main__":
  main()







