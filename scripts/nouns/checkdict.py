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
#~ import verbdict_functions  as vdf
import csvdict
import pyarabic.araby as ar
from pyarabic.arabrepr import arepr
def verify_tashkeel(word):
    """ verify tashkeel on vocalized word"""
    letters, marks = ar.separate(word)
    new_word  = ar.joint(letters, marks)
    return new_word == word
class checkDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)
        self.index = []
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "--" + "\n--".join(self.headerlines) +"\n" 
        line +=  "#" + "Error\t"+u"\t".join(self.display_order)      
        return line
               
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id +=1
        fields = self.treat_tuple(verb_row)
        result = self.check_fields(fields)
        if result != "ok":
            #~ line = u'\t'.join([result, fields.get('vocalized','')])
            #~ line += "\n"+arepr(fields).decode('utf8')
            items=[result,];
            for k in range(len(self.display_order)):
                key = self.display_order[k];
                # some fields are integer, than we use str
                items.append(str(fields[key]))
            line = u"\t".join(items);
        else:
            line =""
        return line        
        
    def check_fields(self, fields):
        """ check fields """
        voc = fields.get('vocalized','')
        if not voc:
            return "Error: Empty vocalized"
        if not ar.is_arabicword(voc):
            return "Error: Invalid Arabic word "
        # not duplicated
        if voc in self.index:
            return "Error: Duplicated Entry "
        self.index.append(voc)
        # valid verb form
        if not ar.is_vocalized(voc):
            return "Error: Not Vocalized" 
        # valid vocalization
        if not verify_tashkeel(voc):
            return "Error: Error in Vocalization "        
        return "ok"
        
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        
        return """"""
