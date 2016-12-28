#!/usr/bin/python2
# -*- coding=utf-8 -*-
#************************************************************************
# $Id: spellverbconst.py,v 0.7 2010/12/26 01:10:00 Taha Zerrouki $
#
# ------------
# Description:
# ------------
#  Copyright (c) 2009, Arabtechies, Arabeyes Taha Zerrouki
#
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2009/06/02 01:10:00 $
#  $Author: Taha Zerrouki $
#  $Revision: 0.7 $
#  $Source: arabtechies.sourceforge.net
#
#***********************************************************************/

from libqutrub.verb_const import *
# table of suffixes of double transitive verbs
#جدةل لواحق الفعل  القلبي المتعدي لمغعول به عاقل، 
TabSuffixesPronominale={
PronounAna     :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'1'},
PronounNahnu   :{'full': u"    HcHdHeHfHgHhHi".replace(' ','') ,'alias':'2'},
PronounAnta    :{'full': u"  HbHcHd  HfHg  Hi".replace(' ','') ,'alias':'3'},
PronounAnti    :{'full': u"  HbHc  HeHfHgHhHi".replace(' ','') ,'alias':'4'},
PronounAntuma  :{'full': u"  HbHc  HeHfHgHhHi".replace(' ','') ,'alias':'5'},
PronounAntuma_f:{'full': u"  HbHc    HfHgHhHi".replace(' ','') ,'alias':'6'},
PronounAntum     :{'full': u"  HjHk      Ho  Hq".replace(' ','') ,'alias':'7'},
PronounAntunna :{'full': u"  HbHc      HgHhHi".replace(' ','') ,'alias':'8'},
PronounHuwa      :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'9'},
PronounHya     :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'10'},
PronounHuma    :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'11'},
PronounHuma_f  :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'12'},
PronounHum     :{'full': u"  HjHkHlHmHnHoHpHq".replace(' ','') ,'alias':'13'},
PronounHunna   :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'14'},
}

#جدةل لواحق الفعل  غير قلبي المتعدي 

TabSuffixes={
PronounAna     :{'full': u"      HdHeHfHgHhHi".replace(' ','') ,'alias':'15'},
PronounNahnu   :{'full': u"      HdHeHfHgHhHi".replace(' ','') ,'alias':'16'},
PronounAnta    :{'full': u"  HbHc          Hi".replace(' ','') ,'alias':'17'},
PronounAnti    :{'full': u"  HbHc          Hi".replace(' ','') ,'alias':'18'},
PronounAntuma  :{'full': u"  HbHc          Hi".replace(' ','') ,'alias':'19'},
PronounAntuma_f:{'full': u"  HbHc          Hi".replace(' ','') ,'alias':'20'},
PronounAntum     :{'full': u"  HjHk          Hq".replace(' ','') ,'alias':'21'},
PronounAntunna :{'full': u"  HbHc          Hi".replace(' ','') ,'alias':'22'},
PronounHuwa      :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'23'},
PronounHya     :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'24'},
PronounHuma    :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'25'},
PronounHuma_f  :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'26'},
PronounHum     :{'full': u"  HjHkHlHmHnHoHpHq".replace(' ','') ,'alias':'27'},
PronounHunna   :{'full': u"  HbHcHdHeHfHgHhHi".replace(' ','') ,'alias':'28'},
}

TabPrefixes={
# const for Tense Name
TensePast                    :{'full': u"PaPbPc  PePfPg      ".replace(' ','') ,'alias':'29'},
TenseFuture                  :{'full': u"PaPbPc  PePfPg    Pj".replace(' ','') ,'alias':'30'},
TenseImperative              :{'full': u"  Pb    Pe          ".replace(' ','') ,'alias':'31'},
TenseConfirmedImperative     :{'full': u"  Pb    Pe          ".replace(' ','') ,'alias':'32'},
TenseJussiveFuture           :{'full': u"  Pb    Pe      Pi  ".replace(' ','') ,'alias':'33'},
TenseSubjunctiveFuture       :{'full': u"  Pb  PdPe    Ph    ".replace(' ','') ,'alias':'34'},
TenseConfirmedFuture         :{'full': u"PaPbPc  PePfPg      ".replace(' ','') ,'alias':'35'},


TensePassivePast             :{'full': u"PaPbPc  PePfPg      ".replace(' ','') ,'alias':'36'},
TensePassiveFuture           :{'full': u"PaPbPc  PePfPg    Pj".replace(' ','') ,'alias':'37'},
TensePassiveJussiveFuture    :{'full': u"  Pb    Pe      Pi  ".replace(' ','') ,'alias':'38'},
TensePassiveSubjunctiveFuture:{'full': u"  Pb  PdPe    Ph    ".replace(' ','') ,'alias':'39'},
TensePassiveConfirmedFuture  :{'full': u"PaPbPc  PePfPg      ".replace(' ','') ,'alias':'40'},
}

# table of suffixes of double transitive verbs
#جدةل لةاحق الفعل المتعدي لمغعولين
TabDisplayTagDouble={
PronounAna       :{'full': u"HbHc",'alias':'41'},
PronounNahnu     :{'full': u"HbHc",'alias':'42'},
PronounAnta      :{'full': u"HbHd",'alias':'43'},
PronounAnti      :{'full': u"HbHd",'alias':'44'},
PronounAntuma  :{'full': u"HbHd",'alias':'45'},
PronounAntuma_f:{'full': u"HbHd",'alias':'46'},
PronounAntum   :{'full': u"HbHd",'alias':'47'},
PronounAntunna :{'full': u"HbHd",'alias':'48'},
PronounHuwa    :{'full': u"HbHcHd",'alias':'49'},
PronounHya     :{'full': u"HbHcHd",'alias':'50'},
PronounHuma    :{'full': u"HbHcHd",'alias':'51'},
PronounHuma_f  :{'full': u"HbHcHd",'alias':'52'},
PronounHum     :{'full': u"HbHcHd",'alias':'53'},
PronounHunna   :{'full': u"HbHcHd",'alias':'54'},
}


CodePronoun={
PronounAna     :'1',
PronounNahnu   :'2',
PronounAnta    :'3',
PronounAnti    :'4',
PronounAntuma  :'5',
PronounAntuma_f:'6',
PronounAntum   :'7',
PronounAntunna :'8',
PronounHuwa    :'9',
PronounHya     :'10',
PronounHuma    :'11',
PronounHuma_f  :'12',
PronounHum     :'13',
PronounHunna   :'14',
}


CodeTense={
# const for Tense Name
TensePast                    :'1',
TenseFuture                  :'2',
TenseImperative              :'3',
TenseConfirmedImperative     :'4',
TenseJussiveFuture           :'5',
TenseSubjunctiveFuture       :'6',
TenseConfirmedFuture         :'7',
TensePassivePast             :'8',
TensePassiveFuture           :'9',
TensePassiveJussiveFuture    :'10',
TensePassiveSubjunctiveFuture:'11',
TensePassiveConfirmedFuture  :'12',
}
