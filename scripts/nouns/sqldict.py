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

class SqlDict(csvdict.CsvDict):
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
        line = "--" + "\n--".join(self.headerlines)  + "\n" 
        line += u"""CREATE TABLE  IF NOT EXISTS `nouns` (
          `id` int(11) unique,
          `vocalized` varchar(30) DEFAULT NULL,
          `unvocalized` varchar(30) DEFAULT NULL,
          `normalized` varchar(30) DEFAULT NULL,
          `stamped` varchar(30) DEFAULT NULL,
          `wordtype` varchar(30) DEFAULT NULL,
          `root` varchar(10) DEFAULT NULL,
          `wazn` varchar(30) DEFAULT NULL,
          `category` varchar(30) DEFAULT NULL,
          `original` varchar(30) DEFAULT NULL,
          `gender` varchar(30) DEFAULT NULL,
          `feminin` varchar(30) DEFAULT NULL,
          `masculin` varchar(30) DEFAULT NULL,
          `number` varchar(30) DEFAULT NULL,
          `single` varchar(30) DEFAULT NULL,
          `broken_plural` varchar(30) DEFAULT NULL,            
          `defined` tinyint(1) DEFAULT 0,
          `mankous` tinyint(1) DEFAULT 0,
          `feminable` tinyint(1) DEFAULT 0,
          `dualable` tinyint(1) DEFAULT 0,
          `masculin_plural` tinyint(1) DEFAULT 0,
          `feminin_plural` tinyint(1) DEFAULT 0,
          `mamnou3_sarf` tinyint(1) DEFAULT 0,
          `relative` tinyint(1) DEFAULT 0,
          `w_suffix` tinyint(1) DEFAULT 0,
          `hm_suffix` tinyint(1) DEFAULT 0,
          `kal_prefix` tinyint(1) DEFAULT 0,
          `ha_suffix` tinyint(1) DEFAULT 0,
          `k_prefix` tinyint(1) DEFAULT 0,
          `annex` tinyint(1) DEFAULT 0,
          `definition` text,
          `note` text
        ) ;"""
        return line
               
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id +=1
        fields = self.treat_tuple(noun_row)
        # to reduce the sql file size, 
        # doesn't work with multiple files
        line = "insert into nouns values " #%", ".join(self.display_order);
        fields['id'] = self.id
        items=[];
        items.append(u"%d"%fields['id']);                   
        for key in self.display_order[1:]:
            if key in self.boolean_fields:
                items.append(u"%d"%fields[key]);
            else:
                items.append(u"'%s'"%fields[key]);
        line += u"(%s);"%u", ".join(items);
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
