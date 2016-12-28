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

class SqlDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "--" + "\n--".join(self.headerlines) +"\n"       
        line +=  u"""create table verbs
            (
            id int unique,
            vocalized varchar(30) not null,
            unvocalized varchar(30) not null,
            root varchar(30),
            normalized varchar(30) not null,
            stamped varchar(30) not null,
            future_type varchar(5),
            triliteral  tinyint(1) default 0, 
            transitive  tinyint(1) default 0, 
            double_trans  tinyint(1) default 0, 
            think_trans  tinyint(1) default 0, 
            unthink_trans  tinyint(1) default 0, 
            reflexive_trans  tinyint(1) default 0, 
            past  tinyint(1) default 0, 
            future  tinyint(1) default 0,  
            imperative  tinyint(1) default 0, 
            passive  tinyint(1) default 0,  
            future_moode  tinyint(1) default 0, 
            confirmed  tinyint(1) default 0, 
            PRIMARY KEY (id)
            );"""
        return line
               
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id +=1
        fields = self.treat_tuple(verb_row)
        # to reduce the sql file size, 
        # doesn't work with multiple files
        line = "insert into verbs values " #%", ".join(self.display_order);
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
        
        return """"""
