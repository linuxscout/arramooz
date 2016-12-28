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

class XmlDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, wordtype, version="N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, wordtype, version)        
    def add_header(self,):
        """
        add the header for new dict
        """
        line ="""<?xml version='1.0' encoding='utf8'?>\n"""
        line += "<!--" + "-->\n<!--".join(self.headerlines) + "-->\n"
        line += "<dictionary>"
        return line      
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        fields = self.treat_tuple(noun_row) 
        line="<noun id='%d'>\n"%self.id;
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            if self.display_order[k] != "id":
                if fields[key]:
                    line+=u" <%s>%s</%s>\n"%(key,fields[key],key);
                else:
                    line+=u" <%s/>\n"%(key);                        
        line+=u"</noun>\n";          
        return line

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return "</dictionary>"

