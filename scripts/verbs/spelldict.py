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
import verbdict_functions  as vdf
import pyarabic.araby as araby
import spellverbconst as svconst
import spellverb as vspell
import libqutrub.mosaref_main as msrif
import libqutrub.ar_verb     as v_ar
import libqutrub.verb_valid   as valid
import libqutrub.verb_const   as const

class SpellDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific Hunspell dictionary format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A", ):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)
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
            line += u"#\t\tis invalid verb\n",v['vocalized'].encode("utf8")
        else:
            future_type = v_ar.get_future_type_entree(v['future_type']);
            conjugTable = msrif.do_sarf( v['vocalized'], v['future_type'], v['all'], v['past'],
                                   v['future'], v['passive'], v['imperative'],
                                   v['future_moode'], v['confirmed'], v['transitive'], 
                                   "DICT");
            TableEntries = {}
            if conjugTable: 
                TableEntries = {}

                for tense in conjugTable.keys():
                    for pronoun in conjugTable[tense].keys():
                        if pronoun != const.PronounAntuma_f: 

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
                            word_nm = araby.strip_tashkeel(conjugTable[tense][pronoun]);
                            if TableEntries.has_key(word_nm):
                                TableEntries[word_nm] += flags;
                            else:
                                TableEntries[word_nm] = flags;
                            #print (u'%s/%s\t%s%s'%(ar_strip_marks(conjugTable[tense][pronoun]), flags, word,verb_cat));
                # print element from the TableEntries
                for key in TableEntries.keys():
                    if key!="":
                        line +=u'%s/%s\n'%(key, vspell.unify_flags(TableEntries[key]))               
            
        return line
        
        
    def test_entry(self, verb_tuple):
        """
        Verify entrie
        """     
        print("------------------------------");
        print(u"\t".join(['word', verb_tuple['word']]));
        print(u"\t".join(['future_type', verb_tuple['future_type']]));
        print(u"\t".join(['transitive',str(verb_tuple['transitive']), ]));
        print(u"\t".join(['double_trans',str(verb_tuple['double_trans']), ]));
        print(u"\t".join(['think_trans',str(verb_tuple['think_trans']), ]));
        print(u"\t".join(['unthink_trans',str(verb_tuple['unthink_trans']), ]));
        print(u"\t".join(['reflexive_trans',str(verb_tuple['reflexive_trans']), ]));
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
        print(u"\t".join(['tense', tenses]));
        print("------------------------------");
    
    def add_footer(self):
                """close the data set, used for ending xml, or sql"""
                
                return """"""
