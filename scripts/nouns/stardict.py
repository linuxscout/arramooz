#!/usr/bin/python2
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

class StarDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, wordtype, version="N/A",  sqltype = "sqlite",):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, wordtype, version)
        self.sqltype= sqltype
    def add_header(self,):
        """
        add the header for new dict
        """
        #~ line = "#" + "\n#".join(self.headerlines)  + "\n" 
        line =""
        return line
               
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id +=1
        fields = self.treat_tuple(noun_row)
        line = ""
        # to reduce the sql file size, 
        # doesn't work with multiple files
        if fields["vocalized"]:
            if fields["vocalized"] == fields["unvocalized"]:
                line += fields["vocalized"]
            else:
                line += u"|".join([fields["vocalized"], fields["unvocalized"]]) 
            line += "\n"
            items=[];
            # display
            display_order=[
                'wordtype',
                'root',
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
                'masculin_plural',
                'feminin_plural',
                'broken_plural',
                'mamnou3_sarf',
                'relative',
                'definition',
                ]
            line += u"%s [%s], %s, %s"%(fields["wordtype"], fields["root"],fields["gender"], fields["number"])
            if fields['feminin']:
                line += u"<br>مؤنثه: %s"%fields['feminin']
            if fields['masculin']:
                line += u"<br>مذكره: %s"%fields['masculin']
            if fields['mamnou3_sarf']:
                line += u"<br>%s"%fields['mamnou3_sarf']  
            if fields['broken_plural']:
                line += u"<br>ج:%s"%fields['broken_plural']  
            if fields['definition']:
                line += u"<br>%s"%fields['definition']                
            line += "\n"
            #~ for key in self.display_order[3:]:
                #~ items.append(u"%s:'%s'<br>"%(key, fields[key]));
            #~ line += u"\n%s\n"%u",".join(items);
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
