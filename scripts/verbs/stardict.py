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

class StarDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version="N/A",  sqltype = "sqlite",):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self,  version)
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
            line += u"فعل [%s]"%fields["root"]
            if fields['triliteral']:
                line += u"<br>ثلاثي"
            else:
                line += u"<br>غير ثلاثي"                
            if fields['transitive']:
                line += u"<br>متعد"
            else:
                line += u"<br>لازم"
            if fields['double_trans']:
                line += u"<br>متعد لمفعولين"
            if fields['think_trans'] :
                line += u"<br>متعد لمفعول عاقل"
            if fields['unthink_trans']:
                line += u"<br>متعد لمفعول غير عاقل"
            if fields['reflexive_trans'] :
                line += u"<br>فعل قلبي"
            tenses = []
            if fields['past'] :
                tenses.append( u"الماضي")
            if fields['future']:
                tenses.append( u"المضارغ")
            if fields['imperative'] :
                tenses.append( u"الأمر")
            if fields['passive'] :
                tenses.append( u"المبني للمجهول")
            if fields['confirmed'] :
                tenses.append( u"المؤكد")
            if tenses:
                line += u"<br>يتصرف في :"
                line += ", ".join(tenses)
            line += "\n"
        return line
        

    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
