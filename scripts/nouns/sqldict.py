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


import csvdict
import noundict_functions as ndf

class SqlDict(csvdict.CsvDict):
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
        line = "--" + "\n--".join(self.headerlines)  + "\n" 
        if self.sqltype == "mysql":
           line +=  u"""CREATE TABLE  IF NOT EXISTS `nouns` (
          `id` int(11) unique auto_increment,
          `vocalized` varchar(30) DEFAULT NULL,
          `unvocalized` varchar(30) DEFAULT NULL,
          `wordtype` varchar(30) DEFAULT NULL,
          `root` varchar(30) DEFAULT NULL,
          `original` varchar(30) DEFAULT NULL,
          `mankous` varchar(30) DEFAULT NULL,
          `feminable` varchar(30) DEFAULT NULL,
          `number` varchar(30) DEFAULT NULL,
          `dualable` varchar(30) DEFAULT NULL,
          `masculin_plural` varchar(30) DEFAULT NULL,
          `feminin_plural` varchar(30) DEFAULT NULL,
          `broken_plural` varchar(30) DEFAULT NULL,
          `mamnou3_sarf` varchar(30) DEFAULT NULL,
          `relative` varchar(30) DEFAULT NULL,
          `w_suffix` varchar(30) DEFAULT NULL,
          `hm_suffix` varchar(30) DEFAULT NULL,
          `kal_prefix` varchar(30) DEFAULT NULL,
          `ha_suffix` varchar(30) DEFAULT NULL,
          `k_suffix` varchar(30) DEFAULT NULL,
          `annex` varchar(30) DEFAULT NULL,
          `definition` text,
          `note` text
        )  DEFAULT CHARSET=utf8;"""
        else:
           line += u"""CREATE TABLE  IF NOT EXISTS `nouns` (
          `id` int(11) unique,
          `vocalized` varchar(30) DEFAULT NULL,
          `unvocalized` varchar(30) DEFAULT NULL,
          `normalized` varchar(30) DEFAULT NULL,
          `stamp` varchar(30) DEFAULT NULL,
          `wordtype` varchar(30) DEFAULT NULL,
          `root` varchar(10) DEFAULT NULL,
          `wazn` varchar(30) DEFAULT NULL,
           `category` varchar(30) DEFAULT NULL,
          `original` varchar(30) DEFAULT NULL,
          `defined` varchar(30) DEFAULT NULL,
          `gender` varchar(30) DEFAULT NULL,
          `feminin` varchar(30) DEFAULT NULL,
          `masculin` varchar(30) DEFAULT NULL,
          `mankous` varchar(30) DEFAULT NULL,
          `feminable` varchar(30) DEFAULT NULL,
          `number` varchar(30) DEFAULT NULL,
          `single` varchar(30) DEFAULT NULL,
          `dualable` varchar(30) DEFAULT NULL,
          `masculin_plural` varchar(30) DEFAULT NULL,
          `feminin_plural` varchar(30) DEFAULT NULL,
          `broken_plural` varchar(30) DEFAULT NULL,
          `mamnou3_sarf` varchar(30) DEFAULT NULL,
          `relative` varchar(30) DEFAULT NULL,
          `w_suffix` varchar(30) DEFAULT NULL,
          `hm_suffix` varchar(30) DEFAULT NULL,
          `kal_prefix` varchar(30) DEFAULT NULL,
          `ha_suffix` varchar(30) DEFAULT NULL,
          `k_suffix` varchar(30) DEFAULT NULL,
          `annex` varchar(30) DEFAULT NULL,
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
        line = "insert into nouns (%s) values "%", ".join(self.display_order);
        fields['id'] = self.id
        items=[];           
        for k in range(len(self.display_order)):
            key=self.display_order[k];
            if key == "id":
                items.append(u"%d"%fields[key]);
            else:
                items.append(u"'%s'"%fields[key]);

        line+=u"(%s);"%u",".join(items);
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
