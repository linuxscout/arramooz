# Arramooz
Arabic Dictionary for Morphological analysis

[![downloads]( https://img.shields.io/sourceforge/dt/arramooz.svg)](http://sourceforge.org/projects/arramooz)
[![downloads]( https://img.shields.io/sourceforge/dm/arramooz.svg)](http://sourceforge.org/projects/arramooz)
  
  Developpers:  Taha Zerrouki: http://tahadz.com
    taha dot zerrouki at gmail dot com
  Collect data manually Mohamed Kebdani, Morroco < med.kebdani gmail.com>
  
Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/linuxscout/arramooz/master/AUTHORS.md)
Release  | 0.3
License  |[GPL](https://github.com/linuxscout/arramooz/master/LICENSE)
Tracker  |[linuxscout/arramooz/Issues](https://github.com/linuxscout/arramooz/issues)
Website  |[http://arramooz.sourceforge.net](http://arramooz.sourceforge.net)
Source  |[Github](http://github.com/linuxscout/arramooz)
Download  |[sourceforge](http://arramooz.sourceforge.net)
Feedbacks  |[Comments](https://github.com/linuxscout/arramooz/)
Accounts  |[@Twitter](https://twitter.com/linuxscout)  [@Sourceforge](http://sourceforge.net/projectsarramooz/)
# Description

Arramooz Alwaseet is an open source Arabic dictionary for morphological analyze,
It can help Natural Language processing developers.
This work is generated from the Ayaspell( Arabic spellchecker) brut data, which are collected manually.

This dictionary consists of three parts :

- stop words
- verbs
- Nouns

If you would cite it in academic work, can you use this citation
```
T. Zerrouki‏, Arramooz Alwaseet : Arabic Dictionary for Morphological analysis,  http://arramooz.sourceforge.net/ https://github.com/linuxscout/arramooz
```
or in bibtex format
```bibtex
@misc{zerrouki2011arramooz,
  title={Arramooz Alwaseet : Arabic Dictionary for Morphological analysis},
  author={Zerrouki, Taha},
  url={http://arramooz.sourceforge.net/},
  year={2011}
}
```
## API
The python API is available as [arramooz-pysqlite](http://github.com/linuxscout/arramooz-pysqlite)

## Files formats

Those files are available as :
- Text format (tab separated)
- SQL database
- XML  files.
- StarDict files
- Python + Sqlite libray 

## BUILD Dictionary in multiple format
The source files are data folder as open document speadsheet files, then we can build dictionary with
```
make
```
which will generate xml, sql and text files, and package it in releases folder.


To make Hunspell files only
```
make spell
```

To make SatrDict files only
```
make stardict
```
NOTE: you must use stardict-editor to Compile releases/stardict/arramooz.sdic in babylon format


To modify the version, you can update $VERSION variable in Makefile file.

To clean  releases use:
```
make clean
```
To modify data or updating data you can open files in data/ in libreoffice calc format, clean releases, and do make.

## Stopwords 
The Stop words list is developed in an independent project (see http://arabicstopwords.sourceforge.ne)


## Verbs


### Database description

Field | Description |  وصف
-------------|----------------|-----------------------------------
vocalized |vocalized word|الكلمة مشكولة
unvocalized |unvocalized word |الكلمة غير مشكولة
root |root of the verb|جذر الفعل
future_type |The future mark, used only ofr trilateral verbs|حركة عين الفعل الثلاثي في المضارع
triliteral |the verb is triliteral (3 letters) or not |الفعل ثلاثي/غير ثلاثي
transitive |transitive or not|فعل متعدي/ لازم
double_trans |has double transitivity for two objetcs|متعدي لمفعولين
think_trans|the verb is transitive to human|متعدي للغاقل
unthink_trans  |the verb is transitive to unhuman being|متعدي لغير العاقل
reflexive_trans |pronominal verb|فعل من أفعال القلوب
past  |can be conjugated in past tense |يتصرف في الماضي
future  |can be conjugated in present and future  tense|يتصرف في المضارع
imperative  |can be conjugated in imperative  |يتصرف في الأمر
passive |can be conjugated in passive voice|يتصرف في المبني للمجهول
future_moode |can be conjugated in  future moode (jusive, subjuctive, ) |يتصرف في المضارع المجزوم أو المنصوب
confirmed  |can be conjugated in confirmed  tenses|يتصرف في المؤكد

### SQL format of verb

```SQL
create table verbs
            (
            id int unique,
            vocalized varchar(30) not null,
            unvocalized varchar(30) not null,
            root varchar(30),
            normalized varchar(30) not null,
            stamp varchar(30) not null,
            future_type varchar(5),
            triliteral  tinyint(1) default 0, 
            transitive  tinyint(1) default 0, 
            double_trans  tinyint(1) default 0, 
            think_trans  tinyint(1) default 0, 
            unthink_trans  tinyint(1) default 0, 
            reflexive_trans  tinyint(1) default 0, 
            past  tinyint(1) default 0, 
            future  tinyint(1) default 0,  
            imperative  tinyint(1) default 0, 
            passive  tinyint(1) default 0,  
            future_moode  tinyint(1) default 0, 
            confirmed  tinyint(1) default 0, 
            PRIMARY KEY (id)
            );
```
            
### XML format 

```xml
<?xml version='1.0' encoding='utf8'?>
<dictionary>
<verb future_type='فتحة' triliteral='1' transitive='1' double_trans='0' think_trans='1' unthink_trans='0' reflexive_trans='0' >
 <word>بَرِحَ</word>
 <unvocalized>برح</unvocalized>
 <root>برح</root>
 <tenses past='1' future='1' imperative='0' passive='0' future_moode='1' confirmed='1'/>
</verb>
....
</dictionary>
```
## Nouns

### Database description
 
Field | Description |  وصف
-------------|----------------|-----------------------------------
vocalized|vocalized word|الكلمة مشكولة
unvocalized |unvocalized word|غير مشكولة
wordtype |word type( Noun of Subject, noun of object, …)|نوع الكلمة (اسم فاعل، اسم مفعول، صيغة مبالغة..)
root |word root|جذر الكلمة
category|word category|صنف الكلمة أو قسمها الفرعي
original|original verb or noun (masdar)|مصدر الكلمة فعل او اسم
mankous|if the word is mankous, ends with Yeh|اسم منقوص
feminable |the word accept Teh_marbuta|يقبل تاء التأنيث
defined| the word is defined or not |معرفة
gender|the word gender|نوع أو جنس الكلمة
feminin| the feminin form of the word|مؤنث الكلمة
masculin| the masculin form of the word| مذكر الكلمة
number |the word is sigle, dual or plural|عدد مفرد/مثنى/جمع
single| the single form of the word|مفرد الكلمة
dualable |accept dual suffix|يقبل التثنية
masculin_plural |accept masculine plural|يقبل جمع المذكر السالم
feminin_plural |accept feminin plural|يقبل جمع المؤنث السالم
broken_plural |the irregular plural if exists|جموع تكسيره إن وجدت
mamnou3_sarf |doesnt accept tanwin|ممنوع من الصرف
relative|relative |منسوب يالياء
w_suffix |accept waw suffix|يقبل الاحقة ـو الخاصة بجمع المذكر السالم عند إضافته إلى ما بعده
hm_suffix |accept Heh+Meem suffix|يقبل اللاحقة ـهم
kal_prefix |accept Kaf+Alef+Lam  prefixe|يقبل السابقة كالـ
ha_suffix|accept Heh suffix|يقبل اللاحقة ـه
k_prefix|accept preposition prefixes without "AL" definition article |يقبل سابقة الجر  دون ال التعريف
annex |accept the oral annexation|يقبل الإضافة إلى ما بعده مثل المقيمي الصلاة
definition |word description|شرح الكلمة
note |notes about the dictionary entry.|ملاحظات على المدخل في القاموس

### SQL format of noun

```sql
CREATE TABLE  IF NOT EXISTS `nouns` (
          `id` int(11) unique,
          `vocalized` varchar(30) DEFAULT NULL,
          `unvocalized` varchar(30) DEFAULT NULL,
          `normalized` varchar(30) DEFAULT NULL,
          `stamp` varchar(30) DEFAULT NULL,
          `wordtype` varchar(30) DEFAULT NULL,
          `root` varchar(10) DEFAULT NULL,
          `wazn` varchar(30) DEFAULT NULL,
          `category` varchar(30) DEFAULT NULL,
          `original` varchar(30) DEFAULT NULL,
          `gender` varchar(30) DEFAULT NULL,
          `feminin` varchar(30) DEFAULT NULL,
          `masculin` varchar(30) DEFAULT NULL,
          `number` varchar(30) DEFAULT NULL,
          `single` varchar(30) DEFAULT NULL,
          `broken_plural` varchar(30) DEFAULT NULL,            
          `defined` tinyint(1) DEFAULT 0,
          `mankous` tinyint(1) DEFAULT 0,
          `feminable` tinyint(1) DEFAULT 0,
          `dualable` tinyint(1) DEFAULT 0,
          `masculin_plural` tinyint(1) DEFAULT 0,
          `feminin_plural` tinyint(1) DEFAULT 0,
          `mamnou3_sarf` tinyint(1) DEFAULT 0,
          `relative` tinyint(1) DEFAULT 0,
          `w_suffix` tinyint(1) DEFAULT 0,
          `hm_suffix` tinyint(1) DEFAULT 0,
          `kal_prefix` tinyint(1) DEFAULT 0,
          `ha_suffix` tinyint(1) DEFAULT 0,
          `k_prefix` tinyint(1) DEFAULT 0,
          `annex` tinyint(1) DEFAULT 0,
          `definition` text,
          `note` text
        ) ;
```
### XML format 

```xml
<noun id='60000'>
 <vocalized>بَارٌّ</vocalized>
 <unvocalized>بار</unvocalized>
 <normalized>بار</normalized>
 <stamp>بر</stamp>
 <wordtype>اسم فاعل</wordtype>
 <root>برر</root>
 <wazn/>
 <category/>
 <original/>
 <gender>مذكر</gender>
 <feminin/>
 <masculin/>
 <number>مفرد</number>
 <single/>
 <broken_plural>+ون;+ات;أَبْرَارٌ;بَرَرَةٌ</broken_plural>
 <defined/>
 <mankous/>
 <feminable>1</feminable>
 <dualable>1</dualable>
 <masculin_plural>1</masculin_plural>
 <feminin_plural>1</feminin_plural>
 <mamnou3_sarf/>
 <relative/>
 <w_suffix/>
 <hm_suffix/>
 <kal_prefix/>
 <ha_suffix/>
 <k_prefix/>
 <annex/>
 <definition>". ""تَرَكَ ابْناً بَارّاً"" : صَادِقاً وَصَالِحاً وَمُحْسِناً. ""اِبْنُكَ البارُّ يُحِبُّكَ"</definition>
 <note/>
</noun>
...

</dictionary>
```

## Script Files:

1- generate the abstract dictionary from the brut manual dictionary:
```shell
python2 $SCRIPT/verbs/gen_verb_dict.py -f $DATA_DIR/verbs/verb_dic_data-net.csv > $OUTPUT/verbs.aya.dic
```
2- generate the file format (xml, csv, sql) of  dictionary from verbs.aya.dic
```shell
python2 $SCRIPT/verbs/gen_verb_dict_format.py -o xml -f $OUTPUT/verbs.aya.dic > $OUTPUT/verbs.xml
```

* [scripts/verbs]

    1- verbdict_functions.py : functions to handle verbs dict used in the generation process
    
    2- verbs/gen_verb_dict.py: generate the abstract dictionary from the brut manual dictionary
    
    3- verbs/gen_verb_dict_format.py: generate the file format (xml, csv, sql) of  dictionary from verbs.aya.dic
     
* [scripts/nouns]

    1- noundict_functions.py : functions to handle nouns dict used in the generation process
    
    2- nouns/gen_noun_dict.py: generate the file format (xml, csv, sql) of  dictionary 
    
* [requirement]

    1- libqutrub
    
    2- pyarabic 





Data Files:
=============
This files are used to create ayaspell dictionary for spellchecking
arramooz\verbs\data


File|Description
----|-----------
verb_dic_data-net.csv |     brut data made manually by Mohamed kebdani.
ar_verb_normalized.dict|    A list of arabic verbs, from Qutrub project.
triverbtable.py     |       A list of trilateral verbs, used by Qutrub.
verbs.aya.dic       |       The verb dictionary in abstract format.




