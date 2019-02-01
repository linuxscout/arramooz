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

import re
import time
import pyarabic.araby as araby

STAMP_PAT = re.compile(u"[%s%s%s%s%s%s%s%s%s%s]"% (araby.ALEF, 
        araby.YEH, araby.HAMZA, araby.ALEF_HAMZA_ABOVE, araby.WAW_HAMZA,
         araby.YEH_HAMZA, araby.WAW, araby.ALEF_MAKSURA, araby.ALEF_MADDA, araby.SHADDA), 
         re.UNICODE)   
def decode_tenses(field):
    """
    Decode tenses field
    """
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
    
def stamp(word):
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
    return STAMP_PAT.sub('', word)
    
def yes(bool):
    if bool: return 1;
    else: return 0;
def bool_yes(c):
    if c == "y" or  c == "Y": return True;
    if c == "n" or  c == "N": return False;
    else: return c;
