#!/usr/bin/python
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: generatenoundict.py,v 0.7 2011/03/26 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2011, Arabtechies, Arabeyes Taha Zerrouki
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
import time
import pyarabic.araby as araby
import noundict_functions as ndf
class CsvDict:
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, wordtype, version="N/A"):
        """
        initiate the dict
        """

        self.id = 0
        self.version = version
        self.field_id={
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
        self.display_order=[
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
        self.id = counter_table.get(wordtype, 1);
        self.wordtype = wordtype_table.get(wordtype, "");

        if not wordtype: 
            print "Fatal Error : unsupported wordtype", wordtype;
            exit();
        #generic Header for project
        self.headerlines = [
         "*************************************",
        "Arramooz Arabic dictionary for morphology analysis",
                    "Noun dictionary file",
                    "Wordtype       : %s"%self.wordtype,                    
                    "Version        : %s"%self.version,
                    "Generated at   : %s"%time.strftime("%Y/%m/%d:%H:%M"),                    
                    "Author         : Taha Zerrouki", 
                    "Web            : http://arramooz.sf.net",
                    "Source           : http://github.com/linuxscout/arramooz",                    
                    "*************************************",
                    ]
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n#".join(self.headerlines) + "\n"
        line +=  "#" + u"\t".join(self.display_order)
        return line
         
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id += 1
        fields = self.treat_tuple(noun_row) 
        items=[];
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            items.append(fields[key]);
        line = u"\t".join(items);
        return line
        
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
        
    def __str__(self,):
        """ return string to  """
        pass;

    def treat_tuple(self,tuple_noun):
        """ convert row data to specific fields
        return a dict of fields"""
        self.id+=1;
        #extract field from the noun tuple
        fields={};
        for key in self.field_id.keys():
            try:
                fields[key] = tuple_noun[self.field_id[key]].strip();
            except IndexError:
                print "#"*5, "key error [%s],"%key, self.field_id[key], len(tuple_noun);
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
        fields['wordtype']   = self.wordtype;
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
        fields['stamp'] = ndf.word_stamp(fields['unvocalized'])
        return fields;
