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
import csvdict
import pyarabic.araby as araby
import spell_noun as nspell
VERIFY_INPUT=True;
#~ VERIFY_INPUT=False;
import stem_noun_const as snconst

class SpellDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific Hunspell dictionary format
    the data is big, then every function print string """
    def __init__(self,  wordtype, version = "N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self,wordtype, version)
        self.affixes_list = []
        nb1=0
        nb2=0
        for procletic in snconst.COMP_PREFIX_LIST_MODEL.keys():
            for encletic in snconst.COMP_SUFFIX_LIST_MODEL:
                for suffix in snconst.CONJ_SUFFIX_LIST:
                    pro_nm = araby.strip_tashkeel(procletic)
                    enc_nm = araby.strip_tashkeel(encletic)
                    if u"-".join([pro_nm, enc_nm]) in snconst.COMP_NOUN_AFFIXES:
                        nb1 += 1
                        if nspell.verify_proaffix_affix(procletic, encletic, suffix):
                            nb2 += 1
                            self.affixes_list.append((procletic, encletic, suffix))        
        print nb1, nb2
        self.suffix_tag = {}
        self.flags ={"S":[], "T":[], 'U':[]}        
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n##".join(self.headerlines) +"\n"       
        return line
               
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id +=1
        noun_tuple = self.treat_tuple(noun_row)
        line = ""
        
        # fields are coded as "Y/N" convert it to True/False
        #~ nrecord['confirmed'] =  vdf.bool_yes(nrecord['confirmed']) 
        
        # display fields to ensure corectness

        #~ VERIFY_INPUT =  True;
        if VERIFY_INPUT: 
            self.test_entry(noun_tuple)
        # conjugate noun
        if not noun_tuple or not noun_tuple.get('vocalized',''):
            return ""
        nb = 0
        prefix_table =[]
        suffix_table =[]
        stem_table = []
        flags_table ={}
        for procletic, encletic, suffix in self.affixes_list:
            affix_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags'] \
                      +snconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags'] \
                      +snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags'] 
            #test if the  given word from dictionary accept those
            # tags given by affixes
            # دراسة توافق الزوائد مع خصائص الاسم،
            # مثلا هل يقبل الاسم التأنيث.
            suffix_nm = araby.strip_tashkeel(suffix)
            encletic_nm = araby.strip_tashkeel(encletic)
            
            if nspell.validate_tags(noun_tuple, affix_tags, procletic, encletic_nm, suffix_nm):

                if nspell.is_compatible_proaffix_affix(noun_tuple, procletic, encletic, suffix):
                    vocalized, semi_vocalized, segmented= nspell.vocalize(noun_tuple['vocalized'], procletic,  suffix, encletic)
                    if VERIFY_INPUT: 
                        print (u"\t".join([  segmented,  vocalized])).encode('utf8')
                    nb += 1
                    listfields = segmented.split('-')
                    if len(listfields) == 4:
                        pref = listfields[0]
                        stem = listfields[1]
                        suff = listfields[2]
                        enc = listfields[3]
                        prefix_table.append(pref)
                        suffix_table.append(suff+enc)
                        stem_table.append(stem)
                        #~
                        if not flags_table.has_key(stem):
                            flags_table[stem] = {}
                        pref_tag = snconst.COMP_PREFIX_LIST_MODEL.get(pref, '')
                        if not pref_tag in flags_table[stem]:
                            flags_table[stem][pref_tag] = []
                        flags_table[stem][pref_tag].append(self.get_suffix_tag(suff, enc))
        # display dictionary entry
        for stem in flags_table:
            # if the stem is diffirent from unvocalized word, we put a tag to say its just a stem not a word
            stem_tag =""
            original = ""
            if stem != noun_tuple['unvocalized']:
                stem_tag = "XX"
                original = "st:%s"%noun_tuple['unvocalized']
            for preftag in flags_table[stem]:
                #~ print flags_table[stem][preftag]
                print (u"%s/%s%s%s po:noun %s"%(stem, stem_tag, preftag, u''.join(sorted(set(flags_table[stem][preftag]))), original)).encode('utf8')
        #print nb, len(set(prefix_table)), "pref", len(set(suffix_table)), "suf",   len(set(stem_table)), "stem", (u" ".join(set(stem_table))).encode('utf8')         
        return line
    
    
    def get_suffix_tag(self, suffix, encletic):
        """give the suffix tags"""
        #if the suffix is used before, get its tag from the table
        key = u''.join([suffix, encletic])
        # get tag if exists
        tag = self.suffix_tag.get(key, '')
        
        if not tag:
        # generate a suffix tag
            fields = suffix.split('-')
            # the suffix contain 2 parts internal suffix + encletic
            # if enclitic we use a special tag to differentiacte it
            if encletic:
                nb = len(self.flags['S'])
                tag = "%s%s"%(chr(ord('S')+nb/26), chr(ord('a')+nb%26))
                self.flags['S'].append(tag)
            else:
                nb = len(self.flags['U'])
                tag = "%s%s"%(chr(ord('U')+nb/26), chr(ord('a')+nb%26))
                self.flags['U'].append(tag)
            self.suffix_tag[key] = tag

        return self.suffix_tag[key]
            
        
    def test_entry(self, noun_tuple):
        """
        Verify entrie
        """ 
        self.id += 1
        fields = noun_tuple
        line = ""
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            line += u"\n%s:\t'%s'"%(key, fields[key]);
        print  line.encode('utf8');
    
    def add_footer(self):
                """close the data set, used for ending xml, or sql"""
                # display affixes rules
                pronoun_list = [u"ه", u"ها", u"هما", u"هم", u"هن", u'كما', u'كم', u'كن', u'نا']
                for pref in snconst.COMP_PREFIX_LIST_MODEL:
                    pref_tag = snconst.COMP_PREFIX_LIST_MODEL[pref]
                    print "PFX  %s  Y   1"%pref_tag
                    print ("PFX  %s  0   %s  ."%(pref_tag, pref)).encode('utf8')
                for suffix in sorted(self.suffix_tag):
                    suffix_tag = self.suffix_tag[suffix]
                    suffix_letters = u''.join( self.suffix_tag[suffix].split('-'))
                    nb_rules = 1
                    if suffix.endswith(u"ك"):
                        nb_rules = len(pronoun_list)+1
                    print "SFX  %s  Y   %d"%(suffix_tag,nb_rules)
                    print ("SFX  %s  0   %s  ."%(suffix_tag, suffix)).encode('utf8')  
                    if suffix.endswith(u"ك"):
                        for pronoun in pronoun_list:
                            print ("SFX  %s  0   %s  ."%(suffix_tag, suffix[:-1]+pronoun)).encode('utf8')  
                            
                # print suffix table
                print "self.suffix_tag={",
                for s, t in self.suffix_tag.items():
                    print ("u'%s':'%s',"%(s,t)).encode('utf8')
                print "}"
                return """"""
