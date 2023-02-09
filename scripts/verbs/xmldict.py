#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  xmldict.py
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

#~ import verbdict_functions  as vdf
import csvdict
class XmlDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, version = "N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)        
    def add_header(self,):
        """
        add the header for new dict
        """
        line ="""<?xml version='1.0' encoding='utf8'?>\n"""
        line += "<!--" + "-->\n<!--".join(self.headerlines) + "-->\n"
        line +="""<!DOCTYPE dictionary [
<!ELEMENT dictionary (verb)*>
<!ELEMENT verb (word,unvocalized,root,normalized,stamped,tenses)>
<!ATTLIST verb
        future_type CDATA #REQUIRED
        double_trans (0|1) #REQUIRED
        reflexive_trans (0|1)  #REQUIRED
        think_trans (0|1)  #REQUIRED
        transitive (0|1)  #REQUIRED
        triliteral (0|1)  #REQUIRED
        unthink_trans (0|1)  #REQUIRED>
<!ELEMENT word (#PCDATA)>
<!ELEMENT unvocalized (#PCDATA)>
<!ELEMENT root (#PCDATA)>
<!ELEMENT normalized (#PCDATA)>
<!ELEMENT stamped (#PCDATA)>
<!ELEMENT tenses EMPTY>
<!ATTLIST tenses
        confirmed (0|1) #REQUIRED
        future (0|1) #REQUIRED
        future_moode (0|1) #REQUIRED
        imperative (0|1) #REQUIRED
        passive (0|1) #REQUIRED
        past (0|1) #REQUIRED>
]>"""
        line += "<dictionary>"
        return line
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        vrecord = self.treat_tuple(verb_row) 
        line  =  "<verb "
        line +=   u"future_type='%s' "%vrecord['future_type']
        line +=   u"triliteral='%s' "%vrecord['triliteral']
        line +=   u"transitive='%s' "%vrecord['transitive']
        line +=   u"double_trans='%s' "%vrecord['double_trans']
        line +=   u"think_trans='%s' "%vrecord['think_trans']
        line +=   u"unthink_trans='%s' "%vrecord['unthink_trans']
        line +=   u"reflexive_trans='%s' "%vrecord['reflexive_trans']
        line +=   u">\n";
        line +=   u" <word>%s</word>\n"%vrecord['vocalized']
        line +=   u" <unvocalized>%s</unvocalized>\n"%vrecord['unvocalized']
        line +=   u" <root>%s</root>\n"%vrecord['root']
        line +=   u" <normalized>%s</normalized>\n"%vrecord['normalized']
        line +=   u" <stamped>%s</stamped>\n"%vrecord['stamped']
        line +=   u""" <tenses past='%s' future='%s' imperative='%s' passive='%s' future_moode='%s' confirmed='%s'/>\n"""%(vrecord['past'],
                 vrecord['future'],
                 vrecord['imperative'], 
                 vrecord['passive'], 
                 vrecord['future_moode'],
                 vrecord['confirmed']
                );            
        line +=  "</verb>";       
        return line

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return "</dictionary>"

