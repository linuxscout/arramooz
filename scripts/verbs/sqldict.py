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
#~ import verbdict_functions  as vdf
import csvdict

class SqlDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A",   sqltype = "sqlite"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)
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
            vrecord['triliteral'],
            vrecord['transitive'],
            vrecord['double_trans'],
            vrecord['think_trans'],
            vrecord['unthink_trans'],
            vrecord['reflexive_trans'],
            vrecord['past'],
            vrecord['future'],
            vrecord['imperative'],
            vrecord['passive'],
            vrecord['future_moode'],
            vrecord['confirmed']
            )
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        
        return """"""
