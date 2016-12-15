#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  verbdict_functions.py
#  
#  Copyright 2016 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import re
import time
import pyarabic.araby as araby

STAMP_PAT = re.compile(u"[%s%s%s%s%s%s%s%s%s]"% (araby.ALEF, 
        araby.YEH, araby.HAMZA, araby.ALEF_HAMZA_ABOVE, araby.WAW_HAMZA,
         araby.YEH_HAMZA, araby.WAW, araby.ALEF_MAKSURA, araby.SHADDA), 
         re.UNICODE)   
def decode_tenses(field):
    """
    Decode tenses field
    """
    all=False;
    past=False;
    future=False;
    passive=False;
    imperative=False;
    future_moode=False;
    confirmed=False;
    if field==u"يعملان":
        all=True;
    else:
        if field.find(araby.YEH)>=0:
            past=True;
        if field.find(araby.AIN)>=0:
            future=True;
        if field.find(araby.MEEM)>=0:
            imperative=True;
        if field.find(araby.LAM)>=0:
            passive=True;
        if field.find(araby.ALEF)>=0:
            future_moode=True;
        if field.find(araby.NOON)>=0:
            confirmed=True;
    return (all, past, future, passive, imperative, future_moode, confirmed);
    
def stamp(word):
    """
    generate a stamp for a word, 
    remove all letters which can change form in the word :
        - ALEF, 
        - HAMZA, 
        - YEH, 
        - WAW, 
        - ALEF_MAKSURA
        - SHADDA
    @return: stamped word
    """
    # strip the last letter if is doubled
    if word[-1:] ==  word[-2:-1]:
        word = word[:-1]
    return STAMP_PAT.sub('', word)
    
def yes(bool):
    if bool: return "y";
    else: return "n";

class CsvDict:
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A"):
        """
        initiate the dict
        """
        self.id = 0
        self.version = version
        #generic Header for project
        self.headerlines = [ "*************************************",
        "Arramooz Arabic dictionary for morphology analysis",
                    "Verb dictionary file",
                    "Version        : %s"%self.version,
                    "Generated at   :%s \n"%time.strftime("%Y/%m/%d:%H:%M"),                    
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
        line += u"\t".join(["id", "word", "unvocalized" , "root" , "future_type" ,"triliteral"  , "transitive"  , "double_trans"  , "think_trans"  , "unthink_trans"  , "reflexive_trans"  , "past"  , "future"  ,  "imperative"  ," passive"  , " future_moode"  , "confirmed"])
        return line
         
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id += 1
        vrecord = self.treat_tuple(verb_row) 
        line = u"\t".join([str(self.id),
            vrecord['word'],
            vrecord['unvocalized'],
            vrecord['root'],
            vrecord['normalized'],
            vrecord['stamp'],
            vrecord['future_type'],
            yes(vrecord['triliteral']),
            yes(vrecord['transitive']),
            yes(vrecord['double_trans']),
            yes(vrecord['think_trans']),
            yes(vrecord['unthink_trans']),
            yes(vrecord['reflexive_trans']),
            yes(vrecord['past']),
            yes(vrecord['future']),
            yes(vrecord['imperative']),
            yes(vrecord['passive']),
            yes(vrecord['future_moode']),
            yes(vrecord['confirmed'])
            ]
            )
        return line
        
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
        
    def __str__(self,):
        """ return string to  """
        pass;

    def treat_tuple(self,tuple_verb):
        """ convert row data to specific fields
        return a dict of fields"""
        self.id+=1;
        v = {}  # verb dict of fields
        # word  tri root    future_type transitive  nb_trans    object_type reflexive_type  tenses  model   nb_case verb_cat    suggest
        
        v["word"]       = tuple_verb[0].strip();
        v["unvocalized"] = araby.strip_tashkeel(v['word']);
        v["tri"]        = tuple_verb[1].strip();
        v['root']       = tuple_verb[2].strip();
        v['normalized'] = araby.normalize_hamza(v['unvocalized'])
        v['stamp']      = stamp(v['unvocalized'])
        v['future_type']= tuple_verb[3].strip();
        v['transitive'] = tuple_verb[4].strip();
        v['nb_trans']   = tuple_verb[5].strip();
        v['object_type']= tuple_verb[6].strip();
        v['reflexive_type'] = tuple_verb[7].strip();
        v['tenses']     = tuple_verb[8].strip();
        #v['#model']    = tuple_verb[9].strip();
        v['nb_case']    = tuple_verb[10].strip();
        #v['#verb_cat']     = tuple_verb[11].strip();
        #v['#suggest']  = tuple_verb[12].strip();

        # Adopt fields to the actual program
        #word;
        if v['tri'] == u"ثلاثي":
            v['triliteral'] = True;
        else:
            v['triliteral'] = False;
        #root
        #future_type
        if v['transitive'] != u"متعد":
            v['transitive']      = False;
            v['unthink_trans']   = False;    # متعدي لغير العاقل
            v['think_trans']     = False;          # متعدي للعاقل، تلقائيا اﻷفعال تقبل العاقل
            v['reflexive_trans'] = False;    #فعل قلوب
            v['double_trans']    = False;             #متعدي لمفعولين
        else:
            v['transitive'] =True;
            ## 
            if v['nb_trans'] =="2":
                v['double_trans'] = True;
            else:
                v['double_trans'] = False;
            # TYPE OF THE OBJECT, REASONALBEL, OR NOT
            if v['object_type'] == u"عاقل":
                v['think_trans'] = True;
                v['unthink_trans'] = False;
            elif v['object_type'] == u"غيرع":
                v['think_trans'] = False;
                v['unthink_trans'] = True;
            else:
                v['think_trans'] = False;
                v['unthink_trans'] = False;
            # reflexive object  فعل القلوب المتعدي، أظنني   
        if v['reflexive_type'] == u"قلبي":
            v['reflexive_trans'] = True;
        else:
            v['reflexive_trans'] = False;
        # decode tenses
        v['all'], v['past'], v['future'], v['passive'], v['imperative'], v['future_moode'], v['confirmed'] = decode_tenses(v['tenses']);
        if v['all']:
            v['tenses'] =u"يعملان";
        else:
            v['tenses'] = u"";
            if v['past']: v['tenses'] +=u"ي";
            else: v['tenses'] += "-";
            if v['future'] : v['tenses'] +=u"ع";
            else: v['tenses'] += "-";
            if v['imperative']: v['tenses'] +=u"م";
            else: v['tenses'] += "-";
            if v['passive']: v['tenses'] +=u"ل";
            else: v['tenses'] += u"-";
            if v['future_moode']: v['tenses']+=u"ا";
            else: v['tenses'] += u"-";
            if v['confirmed']: v['tenses']+=u"ن";
            else: v['tenses'] += u"-";
        return v;

class XmlDict(CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, version = "N/A"):
        """
        initiate the dict
        """
        CsvDict.__init__(self, version)        
    def add_header(self,):
        """
        add the header for new dict
        """
        line ="""<?xml version='1.0' encoding='utf8'?>\n"""
        line += "<!--" + "-->\n<!--".join(self.headerlines) + "-->\n"
        line += "<dictionary>"
        return line
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        vrecord = self.treat_tuple(verb_row) 
        line  =  "<verb "
        line +=   u"future_type='%s' "%vrecord['future_type']
        line +=   u"triliteral='%s' "%yes(vrecord['triliteral'])
        line +=   u"transitive='%s' "%yes(vrecord['transitive'])
        line +=   u"double_trans='%s' "%yes(vrecord['double_trans'])
        line +=   u"think_trans='%s' "%yes(vrecord['think_trans'])
        line +=   u"unthink_trans='%s' "%yes(vrecord['unthink_trans'])
        line +=   u"reflexive_trans='%s' "%yes(vrecord['reflexive_trans'])
        line +=   u">\n";
        line +=   " <word>%s</word>\n"%vrecord['word']
        line +=   u" <unvocalized>%s</unvocalized>\n"%vrecord['unvocalized']
        line +=   u" <root>%s</root>\n"%vrecord['root']
        line +=   u""" <tenses past='%s' future='%s' imperative='%s' passive='%s' future_moode='%s' confirmed='%s'/>\n"""%(yes(vrecord['past']),
                yes( vrecord['future']),
                yes( vrecord['imperative']), 
                yes( vrecord['passive']), 
                yes( vrecord['future_moode']),
                yes( vrecord['confirmed'])
                );            
        line +=  "</verb>";       
        return line

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return "</dictionary>"


class SqlDict(CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A",   sqltype = "sqlite"):
        """
        initiate the dict
        """
        CsvDict.__init__(self, version)
        self.sqltype= sqltype
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "--" + "\n--".join(self.headerlines) +"\n"       
        if self.sqltype == "mysql":
            line +=  u"""create table verbs
            (
            id int unique,
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
            );"""
        else:
            line += u"""CREATE TABLE verbs
            (id int unique not null,
            vocalized varchar(30) not null,
            unvocalized varchar(30) not null,
            root varchar(30),
            normalized varchar(30) not null,
            stamped varchar(30) not null,
            future_type varchar(5),
            triliteral  varchar(2) NOT NULL default 'y', 
            transitive  varchar(2) NOT NULL default 'y', 
            double_trans  varchar(2) NOT NULL default 'y', 
            think_trans  varchar(2) NOT NULL default 'y', 
            unthink_trans  varchar(2) NOT NULL default 'y', 
            reflexive_trans  varchar(2) NOT NULL default 'y', 
            past  varchar(2) NOT NULL default 'y', 
            future  varchar(2) NOT NULL default 'y',  
            imperative  varchar(2) NOT NULL default 'y', 
            passive  varchar(2) NOT NULL default 'y',  
            future_moode  varchar(2) NOT NULL default 'y', 
            confirmed  varchar(2) NOT NULL default 'y', 
            PRIMARY KEY (id)
            );"""
        return line
               
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id +=1
        vrecord = self.treat_tuple(verb_row)
        #(vocalized, unvocalized, root, normalized, stamp, future_type, triliteral, transitive, double_trans, think_trans, unthink_trans, reflexive_trans, past, future, imperative, passive, future_moode, confirmed)
        line = u"insert into verbs ";
        line += u"values ('%d','%s','%s','%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s', '%s', '%s', '%s','%s','%s','%s', '%s');"%(self.id, 
            vrecord['word'],
            vrecord['unvocalized'],
            vrecord['root'],
            vrecord['normalized'],
            vrecord['stamp'],
            vrecord['future_type'],
            yes(vrecord['triliteral']),
            yes(vrecord['transitive']),
            yes(vrecord['double_trans']),
            yes(vrecord['think_trans']),
            yes(vrecord['unthink_trans']),
            yes(vrecord['reflexive_trans']),
            yes(vrecord['past']),
            yes(vrecord['future']),
            yes(vrecord['imperative']),
            yes(vrecord['passive']),
            yes(vrecord['future_moode']),
            yes(vrecord['confirmed'])
            )
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
