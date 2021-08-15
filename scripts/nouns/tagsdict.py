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
import os
import csvdict
import pyarabic.araby as araby
import mysam.tag_const as tconst
import pyarabic.araby as araby
import spell_noun as nspell
#~ VERIFY_INPUT=True;
VERIFY_INPUT=False;
import alyahmor.genelex
import alyahmor.aly_stem_noun_const as snconst
import mysam.tagcoder as tagcoder

import spell_noun as nspell

# redefine if here

# added for purpos of spelling generation

COMP_PREFIX_LIST_MODEL={
"":{'tags':(u"", ), "vocalized":(u"", )}, 
#~ u'ب':{'tags':(u'جر', ), "vocalized":(u"بِ", )}, 
#~ u'ال':{'tags':(u'تعريف', ), "vocalized":(u"الْ", )}, 
#~ u'بال':{'tags':(u'جر', u'تعريف', ), "vocalized":(u"بِالْ", )}, 
}
COMP_PREFIX_LIST = list(COMP_PREFIX_LIST_MODEL.keys())

COMP_SUFFIX_LIST_MODEL=[
"",
u'ِي', 
#~ u"كَ",
u"هُ", # Heh + Damma
]; 
class TagsDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific Hunspell dictionary format
    the data is big, then every function print string """
    def __init__(self,  wordtype, version = "N/A"):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self,wordtype, version)
        # ~ self.affixes_list = []
        nb1=0
        nb2=0
        file_conf = os.path.join( os.path.dirname(__file__), "config/tag.config")        
        self.tagcoder   = tagcoder.tagCoder(file_conf)
        self.affixer = alyahmor.genelex.genelex()
        # costumize affixer affixes
        self.affixer.noun_vocalizer.procletics = COMP_PREFIX_LIST
        self.affixer.noun_vocalizer.enclitics = COMP_SUFFIX_LIST_MODEL
        
        # ~ for procletic in COMP_PREFIX_LIST_MODEL:
            # ~ for encletic in COMP_SUFFIX_LIST_MODEL:
            # ~ #~ for procletic in snconst.COMP_PREFIX_LIST:
            # ~ #~ for encletic in snconst.COMP_SUFFIX_LIST:
                # ~ for suffix in snconst.CONJ_SUFFIX_LIST:
                    # ~ pro_nm = araby.strip_tashkeel(procletic)
                    # ~ enc_nm = araby.strip_tashkeel(encletic)
                    # ~ if u"-".join([pro_nm, enc_nm]) in snconst.COMP_NOUN_AFFIXES:
                        # ~ nb1 += 1
                        # ~ if nspell.verify_proaffix_affix(procletic, encletic, suffix):
                            # ~ nb2 += 1
                            # ~ self.affixes_list.append((procletic, encletic, suffix))        
        # ~ print(nb1, nb2)
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
        if not noun_tuple or not noun_tuple.get('vocalized', ''):
            return ""
        nb = 0
        lines = []
        # replace it by alyahmor.noun_affixer
        lemma = noun_tuple.get('vocalized', '')
        noun_forms = self.affixer.generate_forms( lemma, word_type="noun", details=True)
        for nform_dict in  noun_forms:

            unvocalized =  nform_dict.get("unvocalized", "")
            # lemma from noun_tuple
            lemma_nm = noun_tuple['unvocalized']
            # tags have affix tags + noun tags
            affix_tags = nform_dict.get("tags", "").split(":")
            tags = self.get_tags(noun_tuple,  affix_tags )
            
            lines.append(u"\t".join([unvocalized, lemma_nm, tags]))

        return u"\n".join(set(lines))
    # ~ def add_record2(self, noun_row):
        # ~ """
        # ~ Add a new to the dict
        # ~ """
        # ~ self.id +=1
        # ~ noun_tuple = self.treat_tuple(noun_row)
        # ~ line = ""
        # ~ # fields are coded as "Y/N" convert it to True/False
        # ~ # display fields to ensure corectness
        # ~ if VERIFY_INPUT: 
            # ~ self.test_entry(noun_tuple)
        # ~ # conjugate noun
        # ~ if not noun_tuple or not noun_tuple.get('vocalized', ''):
            # ~ return ""
        # ~ nb = 0
        # ~ lines = []

        # ~ # decrecated         
        # ~ for procletic, encletic, suffix in self.affixes_list:
            # ~ affix_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags'] \
                      # ~ +snconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags'] \
                      # ~ +snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags'] 
            # ~ #test if the  given word from dictionary accept those
            # ~ # tags given by affixes
            # ~ # دراسة توافق الزوائد مع خصائص الاسم،
            # ~ # مثلا هل يقبل الاسم التأنيث.
            # ~ #~ suffix_nm = araby.strip_tashkeel(suffix)
            # ~ encletic_nm = araby.strip_tashkeel(encletic)
            
            # ~ if nspell.validate_tags(noun_tuple, affix_tags, procletic, encletic_nm, suffix):
                # ~ if nspell.is_compatible_proaffix_affix(noun_tuple, procletic, encletic, suffix):
                    # ~ vocalized, semi_vocalized, segmented = nspell.vocalize(noun_tuple['vocalized'], procletic,  suffix, encletic)
                    # ~ tags = self.get_tags(noun_tuple, affix_tags) 
                    
                    # ~ if VERIFY_INPUT: 
                        # ~ print(u"\t".join([  araby.strip_tashkeel(vocalized),  noun_tuple['unvocalized'], tags]))
                        # ~ print("*" + u"\t".join([  araby.strip_tashkeel(vocalized),  noun_tuple['unvocalized'], u','.join(affix_tags)]))
                    # ~ lines.append(u"\t".join([araby.strip_tashkeel(vocalized),  noun_tuple['unvocalized'], tags]))
                    # ~ #~ print "tagsdict",
                    # ~ #~ print(u"\t".join([araby.strip_tashkeel(vocalized), vocalized, noun_tuple['unvocalized'], tags]))

                    # ~ nb += 1
      
        # ~ return u"\n".join(set(lines))
        
    def get_tags(self, noun_tuple, affix_tags):
        """ generate an encoded tag """
        
        tags_list = list(affix_tags)
        if u"جمع مؤنث سالم" in affix_tags:
            tags_list.append(u"مؤنث")
        if not u"مؤنث" in tags_list:
            if u"مؤنث" in noun_tuple['gender']:
                tags_list.append(u"مؤنث")
            if u"مذكر" in noun_tuple['gender']:
                tags_list.append(u"مذكر")
        if u"جمع" in  noun_tuple['number']:
            tags_list.append(u"جمع")
        elif not u"جمع" in affix_tags and not u"مثنى" in affix_tags:
            if u"مفرد" in noun_tuple['number']:
                tags_list.append(u"مفرد")
        elif u"إضافة" in affix_tags and  u"مضاف" in affix_tags:
            tags_list.remove(u"إضافة")
        
            
    
        word_cat = "Noun"
        # wordtype in 
        #~  (u"اسم فاعل", u"اسم مفعول", u"صفة", u"صفة مشبهة", u"صيغة مبالغة",):
        #~ (u"مصدر",):
        #~  (u"علم",):
        #~  (u"جامد", ):
        #~  (u"اسم تفضيل", ):
        tags_list.append(u"اسم")
        wordtypes = noun_tuple['wordtype'].split(':')
        tags_list.extend(wordtypes)
        tags_list.append(word_cat)
        self.tagcoder.reset()
        encoded_tags = self.tagcoder.encode(tags_list)
        #~ from pyarabic.arabrepr import arepr as repr 
        #~ print(repr(tags_list))
        #~ print(encoded_tags)
        return encoded_tags
        
 
    
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
        print(line)
    
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        pass
