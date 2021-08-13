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


import csvdict
import noundict_functions as ndf

class TaksirDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, wordtype, version="N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, wordtype, version)
        self.display_order=[
                'id' ,
                'vocalized' ,
                'unvocalized' ,
                #~ 'normalized' ,
                #~ 'stamped' ,
                'wordtype' ,
                'root' ,
                'wazn' ,
                'category' ,
                #~ 'original' ,
                'gender' ,
                'feminin' ,
                'masculin' ,
                #~ 'number' ,
                #~ 'single' ,
                'broken_plural' ,            
                #~ 'defined' ,
                #~ 'mankous' ,
                'feminable' ,
                #~ 'dualable' ,
                'masculin_plural' ,
                'feminin_plural' ,
                'mamnou3_sarf' ,
                'relative' ,
                #~ 'w_suffix' ,
                #~ 'hm_suffix' ,
                #~ 'kal_prefix' ,
                #~ 'ha_suffix' ,
                #~ 'k_prefix' ,
                #~ 'annex' ,
                'definition',
                'plural_tanwin_nasb',
                'note',
                ]
    def __str__(self,):
        """ return string to  """
        return "TaksirDict Object"   
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n#".join(self.headerlines) + "\n"
        line +=  "#" + u"\t".join(self.display_order)
        return line
    def treat_fields(self, fields):
        """
        Ajust some fields
        """
        # don't include plural
        if fields.get("number","") != u"مفرد":
            return {}
        # remove number field
        fields.pop('number', None)
        return fields;
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id += 1
        fields = self.treat_tuple(noun_row)
        fields = self.treat_fields(fields)
        if not fields:
            return ""       
        items=[];
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            # some fields are integer, than we use str
            items.append(unicode(fields[key]))
        line = u"\t".join(items);
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
