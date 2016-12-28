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




import sys
import re
import time
import pyarabic.araby as araby
# treat the root, strip extra characters
stamp_pat = re.compile(u"[%s%s%s%s%s%s%s%s%s]"% (araby.ALEF, 
araby.YEH, araby.HAMZA, araby.ALEF_HAMZA_ABOVE, araby.WAW_HAMZA,
 araby.YEH_HAMZA, araby.WAW, araby.ALEF_MAKSURA, araby.SHADDA), 
 re.UNICODE)

def word_stamp(word):
    """
    generate a stamp for a word, 
    remove all letters which can change form in the word :
        - ALEF, 
        - HAMZA, 
        - YEH, 
        - WAW, 
        - ALEF_MAKSURA
        - SHADDA
    @return: stamped word
    """
    # strip the last letter if is doubled
    if word[-1:] ==  word[-2:-1]:
        word = word[:-1]
    return stamp_pat.sub('', word)

def decode_root(root):
    root=root.replace(' ','')
    root=root.replace('[','')
    root=root.replace(']','')
    root=root.replace('"','')   
    root=root.replace(TATWEEL,'')
    return root;

# treat the vocalized form, strip extra characters
#deprecated
def decode_vocalized(vocalized):
    vocalized=vocalized.split('-');
    vocalized=vocalized[0].strip();
    vocalized=vocalized.replace(' ','')
    vocalized=vocalized.replace('"','') 
    return vocalized;
# create the mankous form if t's possible
def get_mankous(vocalized):
    if vocalized.endswith( araby.YEH ):
        #strip last yeh
        return vocalized[:-1] + araby.KASRATAN;
    else:
        print (u"*********%s"%vocalized).encode('utf8');
        #exit();
# deprecated
# create the mankous form if t's possible
def get_feminin(vocalized):
    if vocalized[-1:] in (araby.DAMMA, araby.DAMMATAN):
        #strip last yeh
        vocalized=vocalized[:-1];
    return vocalized+FATHA+TEH_MARBUTA+DAMMATAN;
# deprecated
# extract broken plurals from the plural fields
def get_broken_plural(plural):

    broken_plural=plural
    broken_plural=broken_plural.replace(u'ـات','');
    broken_plural=broken_plural.replace(u'ـون','');
    broken_plural=broken_plural.replace(u'ج:','');
    broken_plural=broken_plural.replace(u'.','');   
    broken_plural=broken_plural.replace(u':','');       
    brokens=broken_plural.split(u'،');
    brokensvalid=[];
    for b in brokens:
        b=b.replace(' ','');
        if b!=u"":
            brokensvalid.append(b);
    brokens=u":".join(brokensvalid);
    return brokens;
# deprecated
def get_original(original):
    """Extract the original word from the field"""
    original=original.replace(u')','');
    original=original.replace(u'(',''); 
    original=original.replace(u'"','');     
    return original;


def yes(bool):
    if bool: return "y";
    else: return "n";

