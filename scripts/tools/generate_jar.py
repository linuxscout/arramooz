#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_jar.py
#  
#  Copyright 2020 zerrouki <zerrouki@majd4>
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
enclitics = u"ه|ها|هما|هم|هن|ك|كما|كم|كن|ي|نا".split("|")
enclitics_tags={u'ه':'M1H',
u'ها':'F1H',
u'هما':'M2H',
u'هم':'M3H',
u'هن':'F3H',
u'ك':'M1Y',
u'كما':'M2Y',
u'كم':'M3Y',
u'كن':'F3Y',
u'ي':'M1I',
u'نا':'M3I',

    }
jars = u"في.إلى.من.حول.مع.عند.على.عن.ب.ل".split(".")
for jr in jars:
    print(u"\t".join([jr, jr, "PR-;---;---"]))
    for enc in enclitics:
        form = jr + enc
        
        if jr.endswith(u"ى"):
            form = form.replace(u"ىي",u"ي")
            form = form.replace(u"ى",u"ي")
        form = form.replace(u"عننا",u"عنا")
        form = form.replace(u"مننا",u"منا")
        if not form.endswith(u"يي"):         # حالة في+ي   إليّ، عليّ، تسبب ارتباكا   
            print(u"\t".join([form, jr, "PRD;---;"+enclitics_tags.get(enc,enc)]))
tags = []
for v in enclitics_tags:
    tags.append("PRD;"+enclitics_tags[v])
#~ print("\n".join(sorted(tags)))
