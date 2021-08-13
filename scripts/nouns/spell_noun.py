#!/usr/bin/python2
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------
# Name:        stem_noun
# Purpose:     Arabic lexical analyser, provides feature for 
#~stemming arabic word as noun
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------
"""
    Arabic noun stemmer
"""
import re
import pyarabic.araby as araby
#~ import tashaphyne.stemming
#~ import tashaphyne.normalize
#~ import qalsadi.stem_noun_const as snconst
import alyahmor.aly_stem_noun_const as snconst
#~ import stem_noun_const as snconst
#~ import arramooz.arabicdictionary as arabicdictionary 
#~ import qalsadi.wordcase as wordcase

import spellcache
#~ def logic(field):
    #~ if not field:
        #~ return False
    #~ elif field == "N" or field == "n":
        #~ return False
    #~ else:
        #~ return True
    
def verify_proaffix_affix(procletic, encletic, suffix):
    """
    Verify if proaffixes (sytaxic affixes) are compatable
    with affixes ( conjugation) 
    @param procletic: first level prefix.
    @type procletic: unicode.
    @param encletic: first level suffix.
    @type encletic: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @return: compatible.
    @rtype: True/False.
    """ 
    # avoid Fathatan on no ALEF Tawnwin expect on Teh marbuta and Alef followed by Hamza
    # تجنب تنوين النصب على غير الألف ما عدا التاء المربوطة أو همزة بعد ألف
    #~ if suffix == araby.FATHATAN and not (noun_tuple["unvocalized"].endswith(araby.TEH_MARBUTA) 
        #~ or noun_tuple["unvocalized"].endswith(araby.ALEF+araby.HAMZA) ):
        #~ return False 
    #~ # avoid masculin regular plural with unallowed case
    #~ # تجنب جمع المذكر السالم للكلمات التي لا تقبلها
    #~ if u'جمع مذكر سالم' in snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']\
      #~ and not noun_tuple['masculin_plural']:
        #~ return False;
    #if not procletic and not encletic:  return True
    #use cache for affix verification
    #~ affix = u'-'.join([procletic, encletic, suffix, str(
       #~ bool(noun_tuple['mamnou3_sarf']))])
    affix = u'-'.join([procletic, encletic, suffix])
    #~ #~print affix.encode("utf8")
    if affix in spellcache.cache_affixes_verification:
        return spellcache.cache_affixes_verification[affix]
        
    # get procletics and enclitics tags
    procletic_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags']
    encletic_tags = snconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags']
    # in nouns there is no prefix 
    suffix_tags = snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']        
    # in some cases the suffixes have more cases
    # add this cases to suffix tags
    suffix_tags += snconst.CONJ_SUFFIX_LIST_TAGS[suffix].get("cases",())
    if u"تعريف" in procletic_tags and u"مضاف" in suffix_tags and \
    not u'مضاف' in encletic_tags:
        spellcache.cache_affixes_verification[affix] = False
    #حالة ألف التثنية دون نون مثل كتابا الطالب
    elif u"تعريف" in procletic_tags and u"إضافة" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    elif u"تعريف" in procletic_tags and u"تنوين" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    #~ # التنوين لا يتطابق مع الممنوع من الصرف
    #~ elif ( u'تنوين' in suffix_tags)  and  noun_tuple['mamnou3_sarf']:
        #~ spellcache.cache_affixes_verification[affix] = False
# الجر  في حالات الاسم المعرفة بال أو الإضافة إلى ضمير أو مضاف إليه
# مما يعني لا يمكن تطبيقها هنا
# بل في حالة التحليل النحوي
    elif u"مضاف" in encletic_tags and u"تنوين" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    elif u"مضاف" in encletic_tags and u"لايضاف" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    elif u"جر" in procletic_tags and u"مجرور" not in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
#ستعمل في حالة كسر هاء الضمير في الجر            

    #elif  bool(u"لايجر" in encletic_tags) and  bool(u"مجرور" in \
    #suffix_tags) :
    #    spellcache.cache_affixes_verification[affix] = False
    #elif  bool(u"مجرور" in encletic_tags) and  not bool(u"مجرور" in \
    #suffix_tags) :
    #    spellcache.cache_affixes_verification[affix] = False    
    else:
        spellcache.cache_affixes_verification[affix] = True

    return spellcache.cache_affixes_verification[affix]

def is_compatible_proaffix_affix(noun_tuple, procletic, encletic, suffix):
    """
    Verify if proaffixes (sytaxic affixes) are compatable
    with affixes ( conjugation) 
    @param procletic: first level prefix.
    @type procletic: unicode.
    @param encletic: first level suffix.
    @type encletic: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @return: compatible.
    @rtype: True/False.
    """ 
    # avoid Fathatan on no ALEF Tawnwin expect on Teh marbuta and Alef followed by Hamza
    # تجنب تنوين النصب على غير الألف ما عدا التاء المربوطة أو همزة بعد ألف
    if suffix == araby.FATHATAN and not (noun_tuple["unvocalized"].endswith(araby.TEH_MARBUTA) 
        or noun_tuple["unvocalized"].endswith(araby.ALEF+araby.HAMZA) ):
        return False 
    # avoid masculin regular plural with unallowed case
    # تجنب جمع المذكر السالم للكلمات التي لا تقبلها
    if u'جمع مذكر سالم' in snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']\
      and not noun_tuple['masculin_plural']:
        return False;
    #if not procletic and not encletic:  return True
    #use cache for affix verification
    affix = u'-'.join([procletic, encletic, suffix, str(
       bool(noun_tuple['mamnou3_sarf']))])
    #~print affix.encode("utf8")
    if affix in spellcache.cache_affixes_verification:
        return spellcache.cache_affixes_verification[affix]
        
    # get procletics and enclitics tags
    procletic_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags']
    encletic_tags = snconst.COMP_SUFFIX_LIST_TAGS[encletic]['tags']
    # in nouns there is no prefix 
    suffix_tags = snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']        
    # in some cases the suffixes have more cases
    # add this cases to suffix tags
    suffix_tags += snconst.CONJ_SUFFIX_LIST_TAGS[suffix].get("cases",())
    if u"تعريف" in procletic_tags and u"مضاف" in suffix_tags and \
    not u'مضاف' in encletic_tags:
        spellcache.cache_affixes_verification[affix] = False
    elif u"تعريف" in procletic_tags and u"إضافة" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False        
    elif u"تعريف" in procletic_tags and u"تنوين" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    # التنوين لا يتطابق مع الممنوع من الصرف
    elif ( u'تنوين' in suffix_tags)  and  noun_tuple['mamnou3_sarf']:
        spellcache.cache_affixes_verification[affix] = False
# الجر  في حالات الاسم المعرفة بال أو الإضافة إلى ضمير أو مضاف إليه
# مما يعني لا يمكن تطبيقها هنا
# بل في حالة التحليل النحوي
    elif u"مضاف" in encletic_tags and u"تنوين" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    elif u"مضاف" in encletic_tags and u"لايضاف" in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
    elif u"جر" in procletic_tags and u"مجرور" not in suffix_tags:
        spellcache.cache_affixes_verification[affix] = False
#ستعمل في حالة كسر هاء الضمير في الجر            

    #elif  bool(u"لايجر" in encletic_tags) and  bool(u"مجرور" in \
    #suffix_tags) :
    #    spellcache.cache_affixes_verification[affix] = False
    #elif  bool(u"مجرور" in encletic_tags) and  not bool(u"مجرور" in \
    #suffix_tags) :
    #    spellcache.cache_affixes_verification[affix] = False    
    else:
        spellcache.cache_affixes_verification[affix] = True

    return spellcache.cache_affixes_verification[affix]



def get_stem_variants(stem, suffix_nm):
    """
    Generate the Noun stem variants according to the affixes.
    For example مدرستي = >مدرست+ي = > مدرسة +ي.
    Return a list of possible cases.
    @param stem: the input stem.
    @type stem: unicode.
    @param suffix_nm: suffix (no mark).
    @type suffix_nm: unicode.
    @return: list of stem variants.
    @rtype: list of unicode.
    """
    #some cases must have some correction
    #determinate the  suffix types
    #~suffix = suffix_nm
    
    possible_noun_list = set([stem,])
    if suffix_nm in (araby.ALEF+araby.TEH, araby.YEH+araby.TEH_MARBUTA,
      araby.YEH, araby.YEH+araby.ALEF+araby.TEH):
        possible_noun = stem + araby.TEH_MARBUTA
        possible_noun_list.add(possible_noun)
    if not suffix_nm  or suffix_nm in (araby.YEH+araby.NOON, 
    araby.WAW+araby.NOON):
        possible_noun = stem+araby.YEH
        possible_noun_list.add(possible_noun)
    if stem.endswith(araby.YEH):
        # إذا كان أصل الياء ألفا مقصورة
        possible_noun = stem[:-1]+araby.ALEF_MAKSURA
        possible_noun_list.add(possible_noun)
        
    if stem.endswith(araby.HAMZA):
        possible_noun = stem[:-1]+araby.YEH_HAMZA
        possible_noun_list.add(possible_noun)        
    #to be validated
    validated_list = possible_noun_list
    return validated_list

def get_suffix_variants(word, suffix, enclitic, mankous = False):
    """
    Get the suffix variant to be joined to the word.
    For example: word = مدرس, suffix = ة, encletic = ي. 
    The suffix is converted to Teh.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.        
    @param mankous: if the noun is mankous ends with Yeh منقوص.
    @type mankous: boolean.        
    @return: variant of suffixes  (vocalized suffix and vocalized 
    suffix without I'rab short mark).
    @rtype: (unicode, unicode)
    """
    enclitic_nm = araby.strip_tashkeel(enclitic)
    newsuffix = suffix #default value
    #if the word ends by a haraka
    if suffix.find(araby.TEH_MARBUTA) >= 0 and enclitic_nm:
        newsuffix = re.sub(araby.TEH_MARBUTA, araby.TEH, suffix)

    elif  not enclitic_nm and  araby.is_haraka(suffix):
        if word[-1:] in (araby.YEH, araby.ALEF):
            newsuffix = u""
        elif mankous :
            # the word is striped from YEH المنقوص حذفت ياؤه قبل قليل
            # تحول حركته إلى تنوين كسر
             newsuffix =  araby.KASRATAN
    # if enclitic is Yeh mutakalim ياء المتكلم
    if enclitic_nm == araby.YEH:
        newsuffix = araby.strip_lastharaka(newsuffix)
    #gererate the suffix without I'rab short mark
    # here we lookup with given suffix because the new suffix is 
    # changed and can be not found in table
    if u'متحرك' in snconst.CONJ_SUFFIX_LIST_TAGS[suffix]['tags']:
        suffix_non_irab_mark = araby.strip_lastharaka(newsuffix)
    else:
        suffix_non_irab_mark = newsuffix
    return newsuffix, suffix_non_irab_mark 

def get_enclitic_variant(enclitic_voc, suffix_voc):
    """
    Get the enclitix variant to be joined to the word.
    For example: word = كتاب, suffix = كسرة, encletic = هم. 
    The enclitic has a second form هِم.
    @param enclitic_voc: first level suffix vocalized.
    @type enclitic_voc: unicode.
    @param suffix_voc: second level suffix vocalized.
    @type suffix_voc: unicode.
    @return: variant of enclitic  (vocalized enclitic and vocalized 
    enclitic without I'rab short mark).
    @rtype: (unicode, unicode)
    """
    #print (u"get enclit2 '%s' %d"%(enclitic_voc, len(enclitic_voc))).encode('utf8')
    enclitic_voc_non_inflection_mark = enclitic_voc
    if enclitic_voc.startswith(araby.HEH +  araby.DAMMA) and suffix_voc.endswith(araby.KASRA):
        enclitic_voc_non_inflection_mark = enclitic_voc.replace(araby.HEH +  araby.DAMMA, araby.HEH)
        enclitic_voc = enclitic_voc.replace(araby.HEH +  araby.DAMMA, araby.HEH +  araby.KASRA) 
        #print "ok"
    return enclitic_voc, enclitic_voc_non_inflection_mark 


def get_word_variant(word, suffix, encletic):
    """
    Get the word variant to be joined to the suffix.
    For example: word = مدرسة, suffix = ي. The word is converted to مدرست.
    @param word: word found in dictionary.
    @type word: unicode.
    @param suffix: suffix ( first level).
    @type suffix: unicode.
    @param encletic: encletic( second level).
    @type encletic: unicode.
    @return: variant of word.
    @rtype: unicode.
    """
    word_stem = word
    
    suffix_nm = araby.strip_tashkeel(suffix)

    encletic_nm = araby.strip_tashkeel(encletic)
    long_suffix_nm = suffix_nm + encletic_nm 
    #if the word ends by a haraka
    word_stem = araby.strip_lastharaka(word_stem)
    
    # الاسم المؤنث بالتاء المروبطة نحذفها قبل اللاحقات مثل ات وية
    if word_stem.endswith(araby.TEH_MARBUTA):
        # حالة الاسماء مثل حياة وفتاة
        if word_stem.endswith(araby.ALEF + araby.TEH_MARBUTA):
            if suffix_nm in (araby.YEH, araby.YEH+araby.TEH_MARBUTA, 
         araby.YEH+araby.ALEF+araby.TEH):
                word_stem = word_stem[:-1] + araby.TEH
            elif suffix_nm == araby.ALEF+araby.TEH:
                #نحن بحاجة إلى حذف آخر حركة أيضا
                word_stem = araby.strip_lastharaka(word_stem[:-1])
            elif long_suffix_nm != u"":
                word_stem = word_stem[:-1]+araby.TEH
                
            

        elif suffix_nm in (araby.ALEF+araby.TEH, araby.YEH+araby.TEH_MARBUTA, 
        araby.YEH, araby.YEH+araby.ALEF+araby.TEH):
            #نحن بحاجة إلى حذف آخر حركة أيضا
            word_stem = araby.strip_lastharaka(word_stem[:-1])
        # الاسم المؤنث بالتاء المروبطة نفتحها قبل اللصق
        #مدرسة +ين = مدرستين
        elif long_suffix_nm != u"":
            word_stem = word_stem[:-1]+araby.TEH
       

    elif word_stem.endswith(araby.ALEF_MAKSURA):
        # الاسم المقصور إذا اتصل بلاحقة نحوية صارت ألف المقصورة ياء
        # مستوى +ان = مستويان        
 # إذا كانت اللاحقة الصرفية ذات حروف تتحول الألف المقصورة إلى ياء
         if suffix_nm != u"":
            word_stem = word_stem[:-1]+araby.YEH
        # إذا كانت اللاحقة الصرفية حركات فقط والضمير المتصل  تتحول الألف المقصورة إلى ألف
         elif encletic_nm != u"":
            word_stem = word_stem[:-1]+araby.ALEF 
    elif word_stem.endswith(araby.KASRA + araby.YEH):
     # الاسم المنقوص ينتهي بياء قبلها مكسور
     # إذا كان لا ضمير واللاحقة فقط حركات
     # نحذف ال
         if not encletic_nm  and not suffix_nm :
            word_stem = araby.strip_lastharaka(word_stem[:-2])
     # الاسم المنقوص ينتهي بياء قبلها مكسور
     # إذا كانت اللاحقة ياء ونون
         elif suffix_nm in (araby.YEH + araby.NOON, araby.WAW + araby.NOON) :
            word_stem = araby.strip_lastharaka(word_stem[:-2])


        #ضبط المنتهي بالهمزة حسب حركة اللاحقة النحوية         
    elif word_stem.endswith(araby.HAMZA) and suffix_nm != u"":
        if suffix.startswith(araby.DAMMA):
            word_stem = word_stem[:-1] + araby.WAW_HAMZA
        elif suffix.startswith(araby.KASRA):
            word_stem = word_stem[:-1] + araby.YEH_HAMZA
        elif (word_stem.endswith(araby.YEH + araby.HAMZA) or word_stem.endswith(araby.YEH + araby.SUKUN + araby.HAMZA))and suffix.startswith(araby.FATHATAN):
            word_stem = word_stem[:-1] + araby.YEH_HAMZA            
    return word_stem
        
def vocalize( noun, proclitic,  suffix, enclitic):
    """
    Join the  noun and its affixes, and get the vocalized form
    @param noun: noun found in dictionary.
    @type noun: unicode.
    @param proclitic: first level prefix.
    @type proclitic: unicode.

    @param suffix: second level suffix.
    @type suffix: unicode.
    @param enclitic: first level suffix.
    @type enclitic: unicode.        
    @return: vocalized word.
    @rtype: unicode.
    """
    # procletic have only an uniq vocalization in arabic
    proclitic_voc = snconst.COMP_PREFIX_LIST_TAGS[proclitic]["vocalized"][0]
    # encletic can be variant according to suffix
    #print (u"vocalize: '%s' '%s'"%(enclitic, noun)).encode('utf8')
    enclitic_voc = snconst.COMP_SUFFIX_LIST_TAGS[enclitic]["vocalized"][0]
    enclitic_voc,enclitic_voc_non_inflected  = get_enclitic_variant(enclitic_voc, suffix) 

    suffix_voc = suffix
    #adjust some some harakat
    
    #strip last if tanwin or last harakat
    if araby.is_haraka(noun[-1:]):
        #(DAMMATAN, FATHATAN, KASRATAN, FATHA, DAMMA, KASRA):
        noun = noun[:-1]
    # convert Fathatan into one fatha, in some cases where #
    #the tanwin is not at the end: eg. محتوًى
    noun = noun.replace(araby.FATHATAN, araby.FATHA)

    #add shadda if the first letter is sunny and the procletic 
    #contains AL definition mark
    if (u'تعريف' in snconst.COMP_PREFIX_LIST_TAGS[proclitic]["tags"]\
     and araby.is_sun(noun[0])):
        noun = u''.join([noun[0], araby.SHADDA, noun[1:]])
        #strip the Skun from the lam
        if proclitic_voc.endswith(araby.SUKUN):
            proclitic_voc = proclitic_voc[:-1]
    #completate the dictionary word vocalization
    # this allow to avoid some missed harakat before ALEF
    # in the dictionary form of word, all alefat are preceded by Fatha
    #~noun = araby.complet
    #~ print "stem_noun.vocalize; before", noun.encode('utf8');
    noun = noun.replace(araby.ALEF, araby.FATHA + araby.ALEF)
    #~ print "stem_noun.vocalize; 2", noun.encode('utf8');

    noun = noun.replace(araby.ALEF_MAKSURA, araby.FATHA + araby.ALEF_MAKSURA)
    noun = re.sub(u"(%s)+"%araby.FATHA , araby.FATHA, noun)
    # remove initial fatha if alef is the first letter
    noun = re.sub(u"^(%s)+"%araby.FATHA , "", noun)
    #~ print "stem_noun.vocalize; 3", noun.encode('utf8');
    
    # generate the word variant for some words witch ends by special 
    #letters like Teh_marbuta or Alef_maksura, or hamza, 
    #the variant is influed by the suffix harakat, 
    # for example مدرسة+ي = مدرست+ي
    mankous = True if noun.endswith(araby.KASRA + araby.YEH) else False;
        
    noun = get_word_variant(noun, suffix, enclitic)

    # generate the suffix variant. if the suffix is Teh_marbuta or 
    #Alef_maksura, or hamza, the variant is influed by the enclitic harakat,
    # for example مدرس+ة+ي = مدرس+ت+ي        
    suffix_voc, suffix_non_irab_mark = get_suffix_variants(noun,
     suffix_voc, enclitic, mankous)

    # generate the non vacalized end word: the vocalized word 
    # without the I3rab Mark
    # if the suffix is a short haraka 
    word_non_irab_mark = ''.join([ proclitic_voc,  noun, 
    suffix_non_irab_mark,   enclitic_voc_non_inflected]) 
    # ajust the semivocalized form
    word_non_irab_mark  = re.sub(r"(%s)+"%araby.FATHA , araby.FATHA, word_non_irab_mark )
    word_non_irab_mark  = re.sub(r"(%s%s%s)+"%(araby.FATHA, araby.ALEF_MAKSURA, araby.KASRATAN)
 , araby.FATHATAN + araby.ALEF_MAKSURA, word_non_irab_mark )    
    word_non_irab_mark  = re.sub(r"%s%s%s"%(araby.FATHA, araby.ALEF_MAKSURA, araby.KASRA)
 , araby.FATHA + araby.ALEF_MAKSURA, word_non_irab_mark ) 
    word_non_irab_mark  = re.sub(r"%s[%s|%s|%s]"%(araby.ALEF_MAKSURA, araby.DAMMA, araby.FATHA, araby.KASRA)
 , araby.ALEF_MAKSURA, word_non_irab_mark ) 
    # case of Yeh nisba and Yeh Dhamir
    # حالة الياء الصناعية مع ياء الإضافة للمتكلم
    word_non_irab_mark = re.sub(r"%s(%s)?%s%s$"%(araby.YEH, araby.SHADDA, araby.KASRA, araby.YEH)
     , araby.YEH+araby.SHADDA+araby.FATHA, word_non_irab_mark)    
    #~ word_non_irab_mark =re.sub(ur"%s[%s|%s]%s$"%(araby.YEH, araby.SUKUN, araby.KASRA, araby.YEH)
     #~ , araby.YEH+araby.SHADDA+araby.FATHA, word_non_irab_mark)
    #~ word_non_irab_mark = re.sub(ur"%s%s"%(araby.YEH, araby.YEH)
     #~ , araby.YEH+araby.SHADDA+araby.FATHA, word_non_irab_mark)
    #generate vocalized form
    
    word_vocalized = ''.join([ proclitic_voc, noun, suffix_voc, 
       enclitic_voc])
    #used for spelling purposes
    segmented = '-'.join([ proclitic_voc, noun, suffix_voc, enclitic_voc])
    segmented = araby.strip_tashkeel(segmented)
    #~word_vocalized = araby.ajust_vocalization(word_vocalized)
    word_vocalized = re.sub(r"(%s)+"%araby.FATHA , araby.FATHA, word_vocalized)
    word_vocalized = re.sub(r"%s%s%s"%(araby.FATHA, araby.ALEF_MAKSURA, araby.KASRATAN)
     , araby.FATHATAN + araby.ALEF_MAKSURA, word_vocalized) 
    word_vocalized = re.sub(r"%s%s%s"%(araby.FATHA, araby.ALEF_MAKSURA, araby.DAMMATAN)
     , araby.FATHATAN + araby.ALEF_MAKSURA, word_vocalized) 
    word_vocalized = re.sub(r"%s%s%s"%(araby.FATHA, araby.ALEF_MAKSURA, araby.FATHATAN)
     , araby.FATHATAN + araby.ALEF_MAKSURA, word_vocalized)    
    word_vocalized = re.sub(r"%s%s%s"%(araby.FATHA, araby.ALEF_MAKSURA, araby.KASRA)
     , araby.FATHA + araby.ALEF_MAKSURA, word_vocalized) 
    word_vocalized = re.sub(r"%s[%s|%s|%s]"%(araby.ALEF_MAKSURA, araby.DAMMA, araby.FATHA, araby.KASRA)
     , araby.ALEF_MAKSURA, word_vocalized)
    # case of Yeh nisba and Yeh Dhamir
    # حالة الياء الصناعية مع ياء الإضافة للمتكلم
    word_vocalized = re.sub(r"%s(%s)?%s%s$"%(araby.YEH, araby.SHADDA, araby.KASRA, araby.YEH)
      , araby.YEH+araby.SHADDA+araby.FATHA, word_vocalized)
    #~ word_vocalized = re.sub(r"%s[%s|%s]%s$"%(araby.YEH, araby.SUKUN, araby.KASRA, araby.YEH)
     #~ , araby.YEH+araby.SHADDA+araby.FATHA, word_vocalized)
    #~ word_vocalized = re.sub(r"%s%s$"%(araby.YEH, araby.YEH)
     #~ , araby.YEH+araby.SHADDA+araby.FATHA, word_vocalized)
        
    return word_vocalized, word_non_irab_mark, segmented


def verify_affix(word, list_seg, affix_list):
    """
    Verify possible affixes in the resulted segments according 
    to the given affixes list.
    @param word: the input word.
    @type word: unicode.
    @param list_seg: list of word segments indexes (numbers).
    @type list_seg: list of pairs.
    @return: list of acceped segments.
    @rtype: list of pairs.
    """
    return [s for s in list_seg if '-'.join([word[:s[0]], 
       word[s[1]:]]) in affix_list]

def validate_tags(noun_tuple, affix_tags, procletic, encletic_nm ,
 suffix):
    """
    Test if the given word from dictionary is compabilbe with affixes tags.
    @param noun_tuple: the input word attributes given from dictionary.
    @type noun_tuple: dict.
    @param affix_tags: a list of tags given by affixes.
    @type affix_tags:list.
    @param procletic: first level prefix vocalized.
    @type procletic: unicode.        
    @param encletic_nm: first level suffix vocalized.
    @type encletic_nm: unicode.
    @param suffix: first level suffix vocalized.
    @type suffix: unicode.        
    @return: if the tags are compatible.
    @rtype: Boolean.
    """
    procletic = araby.strip_tashkeel(procletic)
    #~ encletic = encletic_nm
    suffix_nm = araby.strip_tashkeel(suffix)
    #~ print"spell_noun", 
    #~ print(u"\t".join([noun_tuple["vocalized"], procletic, encletic_nm ,
 #~ suffix_nm, u";".join(affix_tags)]).encode('utf8'))
    unvocalized = noun_tuple.get("unvocalized","")

    #~ print((u"تنوين الألف" in affix_tags),unvocalized.endswith(araby.TEH_MARBUTA))


    if  u'تنوين' in affix_tags and  noun_tuple['mamnou3_sarf']:
        return False
    # ألجمع السالم لا يتصل بجمع التكسير
    if  u'جمع مؤنث سالم' in affix_tags and  noun_tuple['number'] in (u'جمع', u'جمع تكسير'):
        return False
    if  u'جمع مذكر سالم' in affix_tags and  noun_tuple['number'] in (u'جمع', u'جمع تكسير'):
        return False        
    if  u'مثنى' in affix_tags and  noun_tuple['number'] in (u'جمع', u'جمع تكسير'):
        return False        
    #~if  u'منسوب' in affix_tags and (not noun_tuple['relative'] and not u'مصدر' in noun_tuple['word_type']):
        #~return False
    #تدقيق الغضافة إلى الضمائر المتصلة
    #~ if encletic_nm == u"هم" and noun_tuple['hm_suffix'] == 'N':
    if encletic_nm == u"هم" and not noun_tuple['hm_suffix']:
        return False
    #~ if encletic_nm == u"ه" and noun_tuple['ha_suffix'] == 'N':
    if encletic_nm == u"ه" and not noun_tuple['ha_suffix'] :
        return False
    #~ if encletic_nm == u"ك" and noun_tuple['k_suffix'] == 'N':
    if procletic == u"ك" and not noun_tuple['k_prefix'] :
        return False
    #حالة قابلية السوابق  مع التعريف
    if procletic.endswith(u"ال") and not noun_tuple['kal_prefix']:
        return False
    # حالة المضاف إلى ما بعهده في حالة جمع المذكر السالم
    # مثل لاعبو، رياضيو
    if suffix_nm == araby.WAW and not noun_tuple['w_suffix']:
        return False
    #التاء المربوطة لا تتصل بجمع التكسير
    if suffix_nm == araby.TEH_MARBUTA and noun_tuple['number'] == u"جمع":
        return False
 
    if u"جمع مذكر سالم" in affix_tags and noun_tuple['number'] == u"جمع":
        return False
    if u"جمع" in affix_tags and noun_tuple['number'] == u"جمع":
        return False
    if u"مثنى" in affix_tags and noun_tuple['number'] == u"جمع":
        return False
    if u"جمع مؤنث سالم" in affix_tags and noun_tuple['number'] == u"جمع":
        return False
    # new verification
    
    if unvocalized.endswith(araby.TEH_MARBUTA):
        #التاء المربوطة لا تتصل بأسم به تاء مربوطة
        if suffix_nm == araby.TEH_MARBUTA:
            return False    
        #تنوين الألف لا يوضع مع اسم منته بتاء مربوطة
        if  u"تنوين الألف" in affix_tags:
            return False
        #لواحق تحمل تاء التأنيث لا ترتبط باسم منته بتاء مربوطة
        if  suffix_nm.startswith(araby.TEH) or  suffix_nm.startswith(u"يت"):
            return False
        # منسوب منوّن بالألف
        if  suffix_nm ==u"يا":
            return False
                
    # elif  u'مضاف' in affix_tags and not noun_tuple['annex']:
        # return False
#todo
    # u'mankous':8, 
# u'feminable':9, *
# u'number':10, 
# u'dualable':11, *
# u'masculin_plural':12, *
# u'feminin_plural':13, *
# u'broken_plural':14, 
# u'mamnou3_sarf':15, 
# u'relative':16, 
# u'w_suffix':17, 
# u'hm_suffix':18, *
# u'kal_prefix':19, *
# u'ha_suffix':20, *
# u'k_suffix':21, *
# u'annex':22, 
    #~ print("spell_noun: True")
    return True

