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
import csvdict
import pyarabic.araby as araby
import spell_noun as nspell
#~ VERIFY_INPUT=True;
VERIFY_INPUT=False;
import stem_noun_const as snconst

class TagsDict(csvdict.CsvDict):
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
        # display fields to ensure corectness
        if VERIFY_INPUT: 
            self.test_entry(noun_tuple)
        # conjugate noun
        if not noun_tuple or not noun_tuple.get('vocalized',''):
            return ""
        nb = 0
        lines = []
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
                    vocalized, semi_vocalized, segmented = nspell.vocalize(noun_tuple['vocalized'], procletic,  suffix, encletic)
                    tags = self.get_tags(noun_tuple, affix_tags) 
                    if VERIFY_INPUT: 
                        print (u"\t".join([  araby.strip_tashkeel(vocalized),  noun_tuple['unvocalized'], tags])).encode('utf8')
                        print ("*" + u"\t".join([  araby.strip_tashkeel(vocalized),  noun_tuple['unvocalized'], u','.join(affix_tags)])).encode('utf8')
                    lines.append(u"\t".join([araby.strip_tashkeel(vocalized),  noun_tuple['unvocalized'], tags]))

                    nb += 1
        return u"\n".join(lines)
        
    def get_tags(self, noun_tuple, affix_tags):
        
        tags = u"-".join(affix_tags);
        prefix = ""
        if u"عطف" in affix_tags:
            prefix +="W"
        else:
            prefix +="-"
        if u"جر" in affix_tags:
            prefix +="B"
        else:
            prefix +="-"            
        if u"تعريف" in affix_tags:
            prefix +="L"
        else:
            prefix +="-"            
        conjug = ""
        if (u"مؤنث" in affix_tags
        or u"مؤنث" in noun_tuple['gender']):
            conjug +="F"
        elif (u"مذكر" in affix_tags
        or u"مذكر" in noun_tuple['gender']):
            conjug +="M"
        else:
            conjug +="-"             
        if (u"جمع" in affix_tags or u"جمع مؤنث سالم" in affix_tags 
            or u"جمع مذكر سالم" in affix_tags
            or u"جمع" in  noun_tuple['number']):
            conjug +="3"
        elif u"مثنى" in affix_tags or noun_tuple["number"] == "3":
            conjug +="2"
        else:
            conjug +="1" 
        
        if u"منصوب" in affix_tags:
            conjug +="A"
        elif u"مرفوع" in affix_tags:
            conjug +="U"            
        elif u"مجرور" in affix_tags:
            conjug +="Y"            
        elif u"مبني" in affix_tags:
            conjug +="B"            
        else:
            conjug +="-" 
            
        encletic = "-"
        if u"مضاف" in affix_tags:
            encletic ="H"            
        # word type coding
        word_cat = "Noun"
        if  noun_tuple['wordtype'] in (u"اسم فاعل", u"اسم مفعول", u"صفة", u"صفة مشبهة", u"صيغة مبالغة",):
            word_cat = "adj"
        elif noun_tuple['wordtype'] in (u"مصدر",):
            word_cat = "masdar"
        elif noun_tuple['wordtype'] in (u"علم",):
            word_cat = "prop_noun"
        elif noun_tuple['wordtype'] in (u"جامد", ):
            word_cat = "jamed"
        elif noun_tuple['wordtype'] in (u"اسم تفضيل", ):
            word_cat = "comparative"
        else:
            word_cat = noun_tuple['wordtype']
            
        tags = "N" +'.' +word_cat+'.'+ ";"+conjug +";"+ prefix + encletic
        return tags
    
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
        pass
