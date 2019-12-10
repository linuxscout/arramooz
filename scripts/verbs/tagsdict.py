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
import verbdict_functions  as vdf
import pyarabic.araby as araby
import spellverbconst as svconst
import spellverb as vspell
import libqutrub.mosaref_main as msrif
import libqutrub.ar_verb     as v_ar
import libqutrub.verb_valid   as valid
import libqutrub.verb_const   as const
import mysam.tagmaker as tagmaker

class TagsDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific Hunspell dictionary format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A", ):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)
        file_conf = os.path.join( os.path.dirname(__file__), "config/tag.config")        
        self.tagmaker   = tagmaker.tagMaker(file_conf)        
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n##".join(self.headerlines) +"\n"       
        return line
               
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id +=1
        v = self.treat_tuple(verb_row)
        line = ""
        
        
        # display fields to ensure corectness
        VERIFY_INPUT=False;
        #~ VERIFY_INPUT =  True;
        if VERIFY_INPUT: 
            self.test_entry(v)

        # conjugate the verb with speling tags
        if not valid.is_valid_infinitive_verb(v['vocalized']):
            line += u"#\t\tis invalid verb \n"
        else:
            future_type = v_ar.get_future_type_entree(v['future_type']);
            conjugTable = msrif.do_sarf( v['vocalized'], v['future_type'], v['all'], v['past'],
                                   v['future'], v['passive'], v['imperative'],
                                   v['future_moode'], v['confirmed'], v['transitive'], 
                                   "DICT");
            TableEntries = {}
            if conjugTable: 
                TableEntries = {}
                tags_info = self.get_verb_info(v)
                for tense in conjugTable.keys():
                    for pronoun in conjugTable[tense].keys():
                        if pronoun != const.PronounAntuma_f: 
                            tags = self.get_tags(tags_info, tense, pronoun)
                            flags = svconst.TabPrefixes[tense]['full'];

                            # the passive tenses dont take object suffix, only with double transitie verbs
                            if (v['transitive'] and tense in const.TableIndicativeTense) or v['double_trans']:#:
                                
                                # add flags for suffixes
                                if v['think_trans'] and v['reflexive_trans']: 
                                    flags += svconst.TabSuffixesPronominale[pronoun]['full'];
                                else:
                                    flags += svconst.TabSuffixes[pronoun]['full'];
                                    
                                #   add flag yeh for the الأفعال الخمسة 
                                if tense == const.TenseFuture and pronoun in (const.PronounAnti, const.PronounAntuma, const.PronounAntuma_f, 
                                                                              const.PronounAntum, const.PronounHuma, const.PronounHuma_f, const.PronounHum ):
                                    flags+=u"Ha"; 
                                                                      
                            # add double object suffixe, if the verb is double transitive, and the tense is indicative 
                            if v['double_trans'] and tense in const.TableIndicativeTense:
                                
                                # add flags for suffixes (double object)
                                    flags += svconst.TabDisplayTagDouble[pronoun]['full'];
                            
                            #add an entree to the table entrie
                            # this allows to reduce many cases into one entree
                            if conjugTable[tense][pronoun]:
                                word_nm = araby.strip_tashkeel(conjugTable[tense][pronoun]);
                                #~ verb_with_shadda = araby.strip_harakat(v['vocalized']);
                                print (u'\t'.join([word_nm, v['vocalized'] , tags])).encode('utf8');
            
        return line
    def get_verb_info(self, verb_tuple):
        """
        Get verb information
        """

        # get verb subclass
        verb_nm = araby.strip_tashkeel(verb_tuple['vocalized'])
        verb_class = ""
        verb_tags = [u"فعل"]
        if verb_nm.startswith(araby.WAW):
            verb_class= "W1W" #"Mithal_W"
            verb_tags.extend([u"معتل", u"مثال", u"واوي"])
        elif verb_nm[-2:-1] ==araby.ALEF: # before last char
            if verb_tuple['future_type'] in (araby.DAMMA, u"ضمة"):
                verb_class= "W2W" #"Adjwaf_W"
                verb_tags.extend([u"معتل", u"أجوف", u"واوي"])                
            elif verb_tuple['future_type'] in (araby.KASRA, u"كسرة"):
                verb_class= "W2Y" #"Adjwaf_Y"
                verb_tags.extend([u"معتل", u"أجوف", u"يائي"])                
        elif verb_nm[-1:]  in (araby.YEH, araby.ALEF_MAKSURA): 
            verb_class= "W3Y" #"Naqis_Y"
            verb_tags.extend([u"معتل", u"ناقص", u"يائي"])                            
        elif verb_nm[-1:]  == araby.ALEF: 
            verb_class= "W3W" #"Naqis_W"
            verb_tags.extend([u"معتل", u"ناقص", u"واوي"])                                        
        elif araby.SHADDA in (verb_tuple['vocalized']): 
            verb_class= "Dbl" # doubled
            verb_tags.append(u"مضعف")            
        else:
            verb_class = "-"
        
        # the passive tenses dont take object suffix, only with double transitie verbs
        tags = "V."+verb_class+"."      
        if verb_tuple['transitive']:
            tags +="T"
            verb_tags.append(u"متعدي")
        else:
            tags +="I"
            verb_tags.append(u"لازم")            
                       
        if verb_tuple['double_trans']:
            tags +="D"
            verb_tags.append(u"متعدي لمفعولين")                        
        elif verb_tuple['think_trans']:
            tags += "T"
            verb_tags.append(u"متعدي للعاقل")                                    
        elif verb_tuple['reflexive_trans']:
            tags += "R"
            verb_tags.append(u"متعدي قلبي")                                                
        # tags pronouns
        else:
            tags +='-'
        #~ return tags        
        return verb_tags        
    def get_tags(self, verb_info, tense, pronoun ):
        """
        Generate tags format
        """
        tags = u";".join(verb_info) + ";"
        tags_list = []
        tags_list.extend(verb_info)
        tags_list.append(tense)
        tags_list.append(pronoun)
        tags += svconst.TabTagsTense[tense]
        tags += svconst.TabTagsPronominale[pronoun]
        
        # add encletic and procletic tags
        #Affixes ( Procletic + Ecletic)
        #Verb procletic :
        #    W: conjonction: starts by WAW or FEH, take 3 values: W: for waw, F; for Feh, -: none.
        #    S: future prefix, س+يتعلم
        tags += ';'
        tags += '-'
        #Verb encletic :
        #define the extended words added to the lexem: الضمائر المضافة
        #    H: if have encletic
        tags += '-'        

        #~ return tags
        encoded_tags = self.tagmaker.encode(tags_list)
        #~ from pyarabic.arabrepr import arepr as repr 
        #~ print(repr(tags_list))
        #~ print(encoded_tags)        
        return encoded_tags
                
    def test_entry(self, verb_tuple):
        """
        Verify entrie
        """     
        print "------------------------------";
        print  (u"\t".join(['word', verb_tuple['word']])).encode('utf8');
        print  (u"\t".join(['future_type', verb_tuple['future_type']])).encode('utf8');
        print  (u"\t".join(['transitive',str(verb_tuple['transitive']), ])).encode('utf8');
        print  (u"\t".join(['double_trans',str(verb_tuple['double_trans']), ])).encode('utf8');
        print  (u"\t".join(['think_trans',str(verb_tuple['think_trans']), ])).encode('utf8');
        print  (u"\t".join(['unthink_trans',str(verb_tuple['unthink_trans']), ])).encode('utf8');
        print  (u"\t".join(['reflexive_trans',str(verb_tuple['reflexive_trans']), ])).encode('utf8');
        if all:
            tenses=u"يعملان";
        else:
            tenses=u"";
            if verb_tuple['past']: tenses+=u"ي";
            else: tenses+="-";
            if verb_tuple['future']: tenses+=u"ع";
            else: tenses+="-";
            if verb_tuple['imperative']: tenses+=u"م";
            else: tenses+="-";
            if verb_tuple['passive']: tenses+=u"ل";
            else: tenses+=u"-";
            if verb_tuple['future_moode']: tenses+=u"ا";
            else: tenses+=u"-";
            if verb_tuple['confirmed']: tenses+=u"ن";
            else: tenses+=u"-";
        print  (u"\t".join(['tense', tenses])).encode('utf8');
        print "------------------------------";
    
    def add_footer(self):
                """close the data set, used for ending xml, or sql"""
                
                return """"""
