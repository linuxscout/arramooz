#!/usr/bin/python2
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: spellverbconst.py,v 0.7 2010/12/26 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
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

import pyarabic.araby as araby
from spellverbconst import *
# table of suffixes of double transitive verbs
#جدةل لواحق الفعل  القلبي المتعدي لمغعول به عاقل، # used to eliminate duplicated flags
def expand_flags(tags):
    
    s=tags;
    count=2;
    listflag=[''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]
    listflag=list(set(listflag));
    listflag.sort();
    return listflag;
# table of suffixes of double transitive verbs
#جدةل لواحق الفعل  القلبي المتعدي لمغعول به عاقل، # used to eliminate duplicated flags
def unify_flags(tags):
    listflag=expand_flags(tags)
    return ''.join(listflag);
    
def decode_tenses(field):
    all=False;
    past=False;
    future=False;
    passive=False;
    imperative=False;
    future_moode=False;
    confirmed=False;
    if field==u"يعملان":
        all=True;
    else:
        if field.find(araby.YEH)>=0:
            past=True;
        if field.find(araby.AIN)>=0:
            future=True;
        if field.find(araby.MEEM)>=0:
            imperative=True;
        if field.find(araby.LAM)>=0:
            passive=True;
        if field.find(araby.ALEF)>=0:
            future_moode=True;
        if field.find(araby.NOON)>=0:
            confirmed=True;
    return (all, past, future, passive, imperative, future_moode, confirmed);
    

    
