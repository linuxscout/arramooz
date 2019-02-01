#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  align_triverbs.py
#  
#  Copyright 2019 zerrouki <zerrouki@majd4>
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
import pyarabic.araby as ar
text=u"""# word;tri;root;bab;future_type;transitive
بَكَمَ;ثلاثي;بكم;3;فتحة;ل
تَمِرَ;ثلاثي;تمر;4;فتحة;ل
حَيِيَ;ثلاثي;حيي;4;فتحة;ل
خَشِبَ;ثلاثي;خشب;4;فتحة;ل
دَحِسَ;ثلاثي;دحس;4;فتحة;ل
رَئِسَ;ثلاثي;رأس;4;فتحة;ل
رَشِحَ;ثلاثي;رشح;4;فتحة;ل
عَاصَ;ثلاثي;عوص;3;فتحة;ل
عَهِرَ;ثلاثي;عهر;4;فتحة;ل
لَبَبَ;ثلاثي;لبب;3;فتحة;ل
لَبِبَ;ثلاثي;لبب;4;فتحة;ل
لَيْسَ;ثلاثي;ليس;3;فتحة;ل
نَغَمَ;ثلاثي;نغم;3;فتحة;ل
هَرَعَ;ثلاثي;هرع;3;فتحة;ل
جَسَدَ;ثلاثي;جسد;3;فتحة;ل
حَضِرَ;ثلاثي;حضر;4;فتحة;ل
حَقَبَ;ثلاثي;حقب;3;فتحة;ل
خَافَ;ثلاثي;خوف;3;فتحة;ل
خَصَرَ;ثلاثي;خصر;3;فتحة;ل
دَهَسَ;ثلاثي;دهس;3;فتحة;ل
سَأَمَ;ثلاثي;جذر;3;فتحة;ل
شَلَحَ;ثلاثي;شلح;3;فتحة;ل
عَيِيَ;ثلاثي;عيي;4;فتحة;ل
فَدَعَ;ثلاثي;فدع;3;فتحة;ل
لَقَحَ;ثلاثي;لقح;3;فتحة;ل
نَامَ;ثلاثي;نوم;3;فتحة;ل
يَمِنَ;ثلاثي;يمن;4;فتحة;ل
بَذُخَ;ثلاثي;بذخ;5;ضمة;ل
تَفَّ;ثلاثي;تفف;1;ضمة;ل
حَبُبَ;ثلاثي;حبب;5;ضمة;ل
حَدُثَ;ثلاثي;حدث;5;ضمة;ل
حَرَا;ثلاثي;حرو;1;ضمة;ل
دَادَ;ثلاثي;دود;1;ضمة;ل
دَاهَ;ثلاثي;دوه;1;ضمة;ل
رَجُنَ;ثلاثي;رجن;5;ضمة;ل
سَمُكَ;ثلاثي;سمك;5;ضمة;ل
شَهُدَ;ثلاثي;شهد;5;ضمة;ل
طَمُثَ;ثلاثي;طمث;5;ضمة;ل
كَهَلَ;ثلاثي;كهل;1;ضمة;ل
كَهُلَ;ثلاثي;كهل;5;ضمة;ل
لَقُنَ;ثلاثي;لقن;5;ضمة;ل
نَكُبَ;ثلاثي;نكب;5;ضمة;ل
نَهُوَ;ثلاثي;نهو;5;ضمة;ل
هَيُؤَ;ثلاثي;هيأ;5;ضمة;ل
وَهُنَ;ثلاثي;وهن;5;ضمة;ل
شَجَعَ;ثلاثي;شجع;1;ضمة;ل
دَرَقَ;ثلاثي;درق;1;ضمة;ل
رَؤُسَ;ثلاثي;رأس;5;ضمة;ل
سَبَلَ;ثلاثي;سبل;1;ضمة;ل
سَفَطَ;ثلاثي;سفط;1;ضمة;ل
ظَرَفَ;ثلاثي;ظرف;1;ضمة;ل
عَرُشَ;ثلاثي;عرش;5;ضمة;ل
فَقَهَ;ثلاثي;فقه;1;ضمة;ل
كَثَلَ;ثلاثي;كثل;1;ضمة;ل
لَبَبَ;ثلاثي;لبب;1;ضمة;ل
نَفَدَ;ثلاثي;نفد;1;ضمة;ل
تَكِئَ;ثلاثي;وكأ;6;كسرة;ل
دَوَى;ثلاثي;دوي;2;كسرة;ل
لَبَبَ;ثلاثي;لبب;2;كسرة;ل
جَنِيَ;ثلاثي;جني;6;كسرة;ل
خَزَى;ثلاثي;خزي;2;كسرة;ل
عَرَى;ثلاثي;عري;2;كسرة;ل
وَدَهَ;ثلاثي;وده;2;كسرة;ل
وَمَقَ;ثلاثي;ومق;2;كسرة;ل
"""

def main(args):
    lines = text.split('\n')
    for line in lines:
        if not line or line.startswith('#'):
            continue
        fields = line.split(';')
        if len(fields)>5:
            verb = fields[0]
            root = fields[2]
            bab = fields[3]
            haraka = fields[4]
            trans = fields[5]
            strg = u"u'%s%s':{'verb':u'%s','root':u'%s','bab':%s,'transitive':u'%s','haraka':u'%s'},"%(verb, bab,verb, root,bab, trans, haraka) 
            print(strg.encode('utf8'))
    idv = 8000
    for line in lines:
        if not line or line.startswith('#'):
            continue
        fields = line.split(';')
        if len(fields)>5:
            verb = fields[0]
            root = fields[2]
            bab = fields[3]
            haraka = fields[4]
            trans = fields[5]
            strg = u';'.join([verb, ar.strip_tashkeel(verb), root,bab,  haraka, trans,"t"+str(idv)]) 
            idv += 1
            print(strg.encode('utf8'))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
