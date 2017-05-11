COMP_PREFIX_LIST_MODEL={
"":{'tags':(u"", ), "vocalized":(u"", )}, 
u'ب':{'tags':(u'جر', ), "vocalized":(u"بِ", )}, 
u'ل':{'tags':(u'جر', ), "vocalized":(u"لِ", )}, 
u'ال':{'tags':(u'تعريف', ), "vocalized":(u"الْ", )}, 
u'بال':{'tags':(u'جر', u'تعريف', ), "vocalized":(u"بِالْ", )}, 
u'لل':{'tags':(u'جر', u'تعريف', ), "vocalized":(u"لِلْ", )}, 
}
COMP_SUFFIX_LIST_MODEL=[
"", 
u'ي', 
u"كَ", 
];                
                # affixes tags contains prefixes and suffixes tags
                affix_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags'] \
                          +snconst.COMP_SUFFIX_LIST_TAGS[encletic_nm]['tags'] \
                          +snconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj_nm]['tags']
                #test if the  given word from dictionary accept those
                # tags given by affixes
                # دراسة توافق الزوائد مع خصائص الاسم،
                # مثلا هل يقبل الاسم التأنيث.
                if validate_tags(noun_tuple, affix_tags, procletic, encletic_nm, suffix_conj_nm):
                    ## get all vocalized form of suffixes
                    for vocalized_encletic in snconst.COMP_SUFFIX_LIST_TAGS[encletic_nm]['vocalized']:
                        for vocalized_suffix in snconst.CONJ_SUFFIX_LIST_TAGS[suffix_conj_nm]['vocalized']:

                         ## verify compatibility between procletics and affix
                            if self.is_compatible_proaffix_affix(noun_tuple, procletic, vocalized_encletic, vocalized_suffix):
                                vocalized, semi_vocalized = vocalize(infnoun, procletic,  vocalized_suffix, vocalized_encletic)

                                #add some tags from dictionary entry as 
                                #mamnou3 min sarf and broken plural
                                original_tags = []
                                if noun_tuple['mankous'] == u"Tk":
                                    original_tags.append(u"منقوص")
                                # get affix tags
                                vocalized_affix_tags = snconst.COMP_PREFIX_LIST_TAGS[procletic]['tags']\
                                  +snconst.COMP_SUFFIX_LIST_TAGS[vocalized_encletic]['tags']\
                                  +snconst.CONJ_SUFFIX_LIST_TAGS[vocalized_suffix]['tags'] 
                                # if there are many cases like feminin plural with mansoub and majrour
                                if 'cases' in snconst.CONJ_SUFFIX_LIST_TAGS[vocalized_suffix]:
                                    list_cases = snconst.CONJ_SUFFIX_LIST_TAGS[vocalized_suffix]['cases']
                                else:
                                   list_cases = ('',)
