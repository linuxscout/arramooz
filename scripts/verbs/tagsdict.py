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
import mysam.tagcoder as tagcoder
import alyahmor.verb_affixer 
import alyahmor.genelex

# redefine if here

# added for purpos of spelling generation
COMP_PREFIX_LIST_TAGS={
"":{'tags':(u"", ), "vocalized":(u"", )}, 
#~ u'ب':{'tags':(u'جر', ), "vocalized":(u"بِ", )}, 
#~ u'ال':{'tags':(u'تعريف', ), "vocalized":(u"الْ", )}, 
#~ u'بال':{'tags':(u'جر', u'تعريف', ), "vocalized":(u"بِالْ", )}, 
}
COMP_PREFIX_LIST = list(COMP_PREFIX_LIST_TAGS.keys())

COMP_SUFFIX_LIST=[
"",
# u"ني",
# u"كَ",
# u"ك",
u"ه", # Heh + Damma
]; 
class TagsDict(csvdict.CsvDict):
    """ a virtual converter of data from table to specific Hunspell dictionary format
    the data is big, then every function print string """
    def __init__(self,  version = "N/A", ):
        """
        initiate the dict
        """
        csvdict.CsvDict.__init__(self, version)
        file_conf = os.path.join( os.path.dirname(__file__), "config/tag.config")        
        self.tagcoder   = tagcoder.tagCoder(file_conf)
        self.verb_affixer = alyahmor.verb_affixer.verb_affixer()
        
        self.affixer = alyahmor.genelex.genelex()

        # costumize affixer affixes
        self.affixer.verb_vocalizer.procletics = COMP_PREFIX_LIST
        self.affixer.verb_vocalizer.enclitics = COMP_SUFFIX_LIST
                   
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n##".join(self.headerlines) +"\n"       
        return line
               
    def add_record2(self, verb_row):
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
                    # the passive tenses dont take object suffix, only with double transitie verbs
                    if (v['transitive'] and tense in const.TableIndicativeTense) or v['double_trans']:
                        accept_attached_pronoun = True
                    else:
                        accept_attached_pronoun = False
                    # browes all pronouns
                    for pronoun in conjugTable[tense].keys():
                        if pronoun != const.PronounAntuma_f: 
                            tags = self.get_tags(tags_info, tense, pronoun)

                            
                            #add an entree to the table entrie
                            # this allows to reduce many cases into one entree
                            if conjugTable[tense][pronoun]:
                                conj = conjugTable[tense][pronoun]
                                word_nm = araby.strip_tashkeel(conj);
                                #~ verb_with_shadda = araby.strip_harakat(v['vocalized']);
                                print (u'\t'.join([word_nm, v['vocalized'] , tags]))
                                # if transitive:
                                if accept_attached_pronoun:
                                    # HEH is used as model for all attached pronoun
                                    verb_attached_pronoun_list = self.verb_affixer.vocalize(conj,"",araby.HEH)
                                    attached = verb_attached_pronoun_list[0][0]
                                    attached = araby.strip_tashkeel(attached)
                                    # add a symbole at the end to mention attached pronoun
                                    #~ attached = attached[:-1] + "h"
                                    tags = self.get_tags(tags_info + [u"ضمير متصل"], tense, pronoun)
                                    print (u'\t'.join([attached, v['vocalized'] , tags]))
            
        return line
    def add_record(self, verb_row):
        """
        Add a new to the dict
        """
        self.id +=1
        v = self.treat_tuple(verb_row)
        tags_info = self.get_verb_info(v)
        lemma = v.get('vocalized', '')           
        lines = []        
        # display fields to ensure corectness
        VERIFY_INPUT=False;
        #~ VERIFY_INPUT =  True;
        if VERIFY_INPUT: 
            self.test_entry(v)

        # conjugate the verb with speling tags
        if not valid.is_valid_infinitive_verb(v.get('vocalized', '')):
            lines.append(u"#\t\tis invalid verb \n")
        else:
            future_mark = v_ar.get_future_type_entree(v['future_type']);
            conjugTable = msrif.do_sarf( v['vocalized'], v['future_type'], v['all'], v['past'],
                                   v['future'], v['passive'], v['imperative'],
                                   v['future_moode'], v['confirmed'], v['transitive'], 
                                   "DICT");

            if conjugTable: 
                # replace it by alyahmor.verb_affixer
                verb_forms = self.affixer.generate_forms(lemma, word_type="verb", details=True, future_type=future_mark)
                for vform_dict in  verb_forms:
                    unvocalized =  vform_dict.get("unvocalized", "")
                    # lemma from noun_tuple
                    # ~ lemma_nm = v['unvocalized']
                    # tags have affix tags + noun tags
                    affix_tags = vform_dict.get("tags", "").split(":")
                    tags = self.get_tags(tags_info,  affix_tags )
                    
                    # lines.append(u"\t".join([unvocalized, lemma, tags, vform_dict.get("tags", "")]))
                    lines.append(u"\t".join([unvocalized, lemma, tags]))
                print(u"\n".join(set(lines)))
                return u"\n".join(set(lines))                
        return ""
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
        if u"معتل" not in verb_tags:
            # verb length
            # length with shadda

            verb_nh = araby.strip_harakat(verb_tuple['vocalized'])
            ln = len(verb_nh)
            
            if ln == 3:
                verb_tags.append(u"ثلاثي")   
                verb_class = "3"                                             
            elif ln == 4:
                verb_tags.append(u"رباعي")                                                
                verb_class = "4"                                                             
            elif ln == 5:
                verb_tags.append(u"خماسي")
                verb_class = "5"
            elif ln == 6:
                verb_tags.append(u"سداسي")
                verb_class = "6"
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
            verb_tags.append(u"متعدي")

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
    def get_tags(self, verb_info, affix_tags ):
        """
        Generate tags format
        """
        tags = u";".join(verb_info) + ";"
        tags_list = []
        tags_list.extend(verb_info)
        tags_list.extend(affix_tags)
        # ~ tags_list.append(pronoun)
        # ~ tags += svconst.TabTagsTense[tense]
        # ~ tags += svconst.TabTagsPronominale[pronoun]
        
        # add encletic and procletic tags
        #Affixes ( Procletic + Ecletic)
        #Verb procletic :
        #    W: conjonction: starts by WAW or FEH, take 3 values: W: for waw, F; for Feh, -: none.
        #    S: future prefix, س+يتعلم
        # ~ tags += ';'
        # ~ tags += '-'
        #Verb encletic :
        #define the extended words added to the lexem: الضمائر المضافة
        #    H: if have encletic
        # ~ print(affix_tags)
        if u"مفعول به" in affix_tags:
            tags_list.append(u"ضمير متصل")
        # ~ else:
            # ~ tags += '-'        

        #~ return tags
        self.tagcoder.reset()        
        encoded_tags = self.tagcoder.encode(tags_list)
        #~ from pyarabic.arabrepr import arepr as repr 
        #~ print(repr(tags_list))
        #~ print(encoded_tags)        
        return encoded_tags
                
    def test_entry(self, verb_tuple):
        """
        Verify entrie
        """     
        print("------------------------------");
        print(u"\t".join(['word', verb_tuple['word']]))
        print(u"\t".join(['future_type', verb_tuple['future_type']]))
        print(u"\t".join(['transitive',str(verb_tuple['transitive']), ]))
        print(u"\t".join(['double_trans',str(verb_tuple['double_trans']), ]))
        print(u"\t".join(['think_trans',str(verb_tuple['think_trans']), ]))
        print(u"\t".join(['unthink_trans',str(verb_tuple['unthink_trans']), ]))
        print(u"\t".join(['reflexive_trans',str(verb_tuple['reflexive_trans']), ]))
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
        print(u"\t".join(['tense', tenses]))
    
    def add_footer(self):
                """close the data set, used for ending xml, or sql"""
                
                return """"""
