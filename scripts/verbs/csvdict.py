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

import time
import pyarabic.araby as araby
import verbdict_functions  as vdf


class CsvDict:
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A"):
        """
        initiate the dict
        """
        self.id = 0
        self.version = version
        #generic Header for project
        self.headerlines = [ "*************************************",
        "Arramooz Arabic dictionary for morphology analysis",
                    "Verb dictionary file",
                    "Version        : %s"%self.version,
                    "Generated at   : %s "%time.strftime("%Y/%m/%d:%H:%M"),                    
                    "Author         : Taha Zerrouki", 
                    "Web            : http://arramooz.sf.net",
                    "Source         : http://github.com/linuxscout/arramooz",
                    "*************************************",
                    ] 
        self.field_id={
                    "vocalized"       : 0, # The word
                    "tri"        : 1, # triletiral or not
                    'root'       : 2, # root
                    'future_type': 3, # future mark 
                    'transitive' : 4, # transitive
                    'nb_trans'   : 5, #  
                    'object_type': 6,
                    'reflexive_type' : 7,
                    'tenses'     : 8,
                    #'#model'    : 9,
                    'nb_case'    : 10,
                    #'#verb_cat'     : 11,
                    #'#suggest'  : 12,        
        }
        #give the display order for text format display
        self.display_order=[
                'id' ,
                'vocalized',
                'unvocalized',
                'root',
                'normalized',
                'stamped',
                'future_type',
                'triliteral',
                'transitive',
                'double_trans',
                'think_trans',
                'unthink_trans',
                'reflexive_trans',
                'past',
                'future',
                'imperative',
                'passive',
                'future_moode',
                'confirmed',
                ]
        self.boolean_fields=[
                'triliteral',
                'transitive',
                'double_trans',
                'think_trans',
                'unthink_trans',
                'reflexive_trans',
                'past',
                'future',
                'imperative',
                'passive',
                'future_moode',
                'confirmed',        
                ]       
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n#".join(self.headerlines) + "\n"
        line +=  "#" + u"\t".join(self.display_order)
        return line
         
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id += 1
        fields = self.treat_tuple(verb_row) 
        items=[];
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            # some fields are integer, than we use str
            items.append(str(fields[key]))
        line = u"\t".join(items);

        return line
        
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
        
    def __str__(self,):
        """ return string to  """
        pass;

    def treat_tuple(self,tuple_verb):
        """ convert row data to specific fields
        return a dict of fields"""
        #~ self.id+=1;
        v = {"id": self.id,}  # verb dict of fields
                
        #extract field from the verb tuple
        for key in self.field_id.keys():
            try:
                v[key] = tuple_verb[self.field_id[key]].strip();
            except IndexError:
                print("#"*5, "key error [%s],"%key, self.field_id[key], len(tuple_verb));

                print(tuple_verb)
                sys.exit()
        v["unvocalized"] = araby.strip_tashkeel(v['vocalized']);
        v['normalized'] = araby.normalize_hamza(v['unvocalized'])
        v['stamped']      = vdf.stamp(v['unvocalized'])

        # Adopt fields to the actual program
        #word;
        if v['tri'] == u"ثلاثي":
            v['triliteral'] = True;
        else:
            v['triliteral'] = False;
        #root
        #future_type
        if v['transitive'] != u"متعد":
            v['transitive']      = False;
            v['unthink_trans']   = False;    # متعدي لغير العاقل
            v['think_trans']     = False;          # متعدي للعاقل، تلقائيا اﻷفعال تقبل العاقل
            v['reflexive_trans'] = False;    #فعل قلوب
            v['double_trans']    = False;             #متعدي لمفعولين
        else:
            v['transitive'] =True;
            ## 
            if v['nb_trans'] =="2":
                v['double_trans'] = True;
            else:
                v['double_trans'] = False;
            # TYPE OF THE OBJECT, REASONALBEL, OR NOT
            if v['object_type'] == u"عاقل":
                v['think_trans'] = True;
                v['unthink_trans'] = False;
            elif v['object_type'] == u"غيرع":
                v['think_trans'] = False;
                v['unthink_trans'] = True;
            else:
                v['think_trans'] = False;
                v['unthink_trans'] = False;
            # reflexive object  فعل القلوب المتعدي، أظنني   
        if v['reflexive_type'] == u"قلبي":
            v['reflexive_trans'] = True;
        else:
            v['reflexive_trans'] = False;
        # decode tenses
        v['all'], v['past'], v['future'], v['passive'], v['imperative'], v['future_moode'], v['confirmed'] = vdf.decode_tenses(v['tenses']);
        if v['all']:
            v['tenses'] =u"يعملان";
        else:
            v['tenses'] = u"";
            if v['past']: v['tenses'] +=u"ي";
            else: v['tenses'] += "-";
            if v['future'] : v['tenses'] +=u"ع";
            else: v['tenses'] += "-";
            if v['imperative']: v['tenses'] +=u"م";
            else: v['tenses'] += "-";
            if v['passive']: v['tenses'] +=u"ل";
            else: v['tenses'] += u"-";
            if v['future_moode']: v['tenses']+=u"ا";
            else: v['tenses'] += u"-";
            if v['confirmed']: v['tenses']+=u"ن";
            else: v['tenses'] += u"-";
            # convert True/false to 0/1
            
        v['triliteral']   = vdf.yes(v['triliteral'])
        v['transitive']   = vdf.yes(v['transitive'])
        v['double_trans'] = vdf.yes(v['double_trans'])
        v['think_trans']  = vdf.yes(v['think_trans'])
        v['unthink_trans'] =  vdf.yes(v['unthink_trans'])
        v['reflexive_trans'] =    vdf.yes(v['reflexive_trans'])
        v['past'] =   vdf.yes(v['past'])
        v['future'] =     vdf.yes(v['future'])
        v['imperative'] =     vdf.yes(v['imperative'])
        v['passive'] =    vdf.yes(v['passive'])
        v['future_moode'] =   vdf.yes(v['future_moode'])
        v['confirmed'] =  vdf.yes(v['confirmed']) 
           
        return v;
