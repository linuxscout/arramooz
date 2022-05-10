#!/usr/bin/env python2
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
import os
import csvdict
import pyarabic.araby as araby
import mysam.tag_const as tconst
import pyarabic.araby as araby
import spell_noun as nspell
#~ VERIFY_INPUT=True;
VERIFY_INPUT=False;
import alyahmor.genelex
import alyahmor.aly_stem_noun_const as snconst


import spell_noun as nspell

# redefine if here

# added for purpos of spelling generation

COMP_PREFIX_LIST_MODEL={
"":{'tags':(u"", ), "vocalized":(u"", )}, 
#~ u'ب':{'tags':(u'جر', ), "vocalized":(u"بِ", )}, 
#~ u'ال':{'tags':(u'تعريف', ), "vocalized":(u"الْ", )}, 
#~ u'بال':{'tags':(u'جر', u'تعريف', ), "vocalized":(u"بِالْ", )}, 
}
COMP_PREFIX_LIST = list(COMP_PREFIX_LIST_MODEL.keys())

COMP_SUFFIX_LIST_MODEL=[
"",
u'ِي', 
#~ u"كَ",
u"هُ", # Heh + Damma
]; 
class WordListDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific Hunspell dictionary format
    the data is big, then every function print string """
    def __init__(self,  wordtype, version = "N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self,wordtype, version)
        self.affixer = alyahmor.genelex.genelex()
        # costumize affixer affixes
        # ~ self.affixer.noun_vocalizer.procletics = COMP_PREFIX_LIST
        # ~ self.affixer.noun_vocalizer.enclitics = COMP_SUFFIX_LIST_MODEL
        

    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n##".join(self.headerlines) +"\n"       
        return line
               
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id +=1
        noun_tuple = self.treat_tuple(noun_row)
        line = ""
        # fields are coded as "Y/N" convert it to True/False
        # display fields to ensure corectness
        if VERIFY_INPUT: 
            self.test_entry(noun_tuple)
        # conjugate noun
        if not noun_tuple or not noun_tuple.get('vocalized', ''):
            return ""
        nb = 0
        lines = []
        # replace it by alyahmor.noun_affixer
        lemma = noun_tuple.get('vocalized', '')
        noun_forms = self.affixer.generate_forms( lemma, word_type="noun", details=True)
        
        for nform_dict in  noun_forms:

            vocalized =  nform_dict.get("vocalized", "")
           
            lines.append(vocalized)

        return u"\n".join(set(lines))
        
 
            
        
    def test_entry(self, noun_tuple):
        """
        Verify entrie
        """ 
        self.id += 1
        fields = noun_tuple
        line = ""
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            line += u"\n%s:\t'%s'"%(key, fields[key]);
        print(line)
    
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        pass
