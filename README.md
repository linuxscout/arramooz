#Arramooz
Arabic Dictionary for Morphological analysis

[![downloads]( https://img.shields.io/sourceforge/dt/arramooz.svg)](http://sourceforge.org/projects/arramooz)
[![downloads]( https://img.shields.io/sourceforge/dm/arramooz.svg)](http://sourceforge.org/projects/arramooz)
  
  Developpers: 	Taha Zerrouki: http://tahadz.com
	taha dot zerrouki at gmail dot com
  
Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/linuxscout/arramooz/master/AUTHORS.md)
Release  | 0.2
License  |[GPL](https://github.com/linuxscout/arramooz/master/LICENSE)
Tracker  |[linuxscout/arramooz/Issues](https://github.com/linuxscout/arramooz/issues)
Website  |[http://arramooz.sourceforge.net](http://arramooz.sourceforge.net)
Source  |[Github](http://github.com/linuxscout/arramooz)
Download  |[sourceforge](http://arramooz.sourceforge.net)
Feedbacks  |[Comments](https://github.com/linuxscout/arramooz/)
Accounts  |[@Twitter](https://twitter.com/linuxscout)  [@Sourceforge](http://sourceforge.net/projectsarramooz/)
#Description

Arramooz Alwaseet is an open source Arabic dictionary for morphological analyze,
It can help Natural Language processing developers.
This work is generated from the Ayaspell( Arabic spellchecker) brut data, which are collected manually.

This dictionary consists of three parts :

- stop words
- verbs
- Nouns

##Files formats

Those files are available as :
- Text format (tab separated)
- SQL database
- XML  files.

##Stopwords 
The Stop words list is developed in an independent project (see http://arabicstopwords.sourceforge.ne)


##Verbs


###Database description

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

###SQL format of verb

```SQL
create table IF NOT EXISTS verbs
			(
			id int unique auto_increment,
			vocalized varchar(30) not null,
			unvocalized varchar(30) not null,
			root varchar(30),
			future_type varchar(5),
			triliteral  ENUM( "n", "y" ) NOT NULL default "y", 
			transitive  ENUM( "n", "y" ) NOT NULL default "y", 
			double_trans  ENUM( "n", "y" ) NOT NULL default "y", 
			think_trans  ENUM( "n", "y" ) NOT NULL default "y", 
			unthink_trans  ENUM( "n", "y" ) NOT NULL default "y", 
			reflexive_trans  ENUM( "n", "y" ) NOT NULL default "y", 
			past  ENUM( "n", "y" ) NOT NULL default "y", 
			future  ENUM( "n", "y" ) NOT NULL default "y",  
			imperative  ENUM( "n", "y" ) NOT NULL default "y", 
			passive  ENUM( "n", "y" ) NOT NULL default "y",  
			future_moode  ENUM( "n", "y" ) NOT NULL default "y", 
			confirmed  ENUM( "n", "y" ) NOT NULL default "y", 
			PRIMARY KEY (id)
			)
```
			
###XML format 

```xml
<?xml version='1.0' encoding='utf8'?>
<dictionary>
<verb  future_type='َ'
	triliteral='True'
	transitive='False'
	double_trans='False'
	think_trans='False'
	unthink_trans='False' 
	reflexive_trans='False' 
>
<word>زُهِيَ</word>
<unvocalized>زهي</unvocalized>
<root>زهو</root>
<tenses past='False' future='False' imperative='False'
	passive='True' future_moode='False' confirmed='False'/>
</verb>
....
</dictionary>
```
##Nouns

###Database description

Field | Description |  وصف
-------------|----------------|-----------------------------------
 vocalized|vocalized word|الكلمة مشكولة
unvocalized |unvocalized word|غير مشكولة
wordtype |word type( Noun of Subject, noun of object, …)|نوع الكلمة (اسم فاعل، اسم مفعول، صيغة مبالغة..)
root |word root|جذر الكلمة
original|original verb or noun (masdar)|مصدر الكلمة فعل او اسم
mankous|if the word is mankous, ends with Yeh|اسم منقوص
feminable |the word accept Teh_marbuta|يقبل تاء التأنيث
number |the word is sigle, dual or plural|عدد مفرد/مثنى/جمع
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
k_suffix|accept Kaf suffix|يقبل اللاحقة ك
annex |accept the oral annexation|يقبل الإضافة إلى ما بعده مثل المقيمي الصلاة
definition |word description|شرح الكلمة
note |notes about the dictionary entry.|ملاحظات على المدخل في القاموس

###SQL format of noun

```sql
CREATE TABLE  IF NOT EXISTS `nouns` (
		  `id` int(11) unique auto_increment,
		  `vocalized` varchar(30) DEFAULT NULL,
		  `unvocalized` varchar(30) DEFAULT NULL,
		  `wordtype` varchar(30) DEFAULT NULL,
		  `root` varchar(30) DEFAULT NULL,
		  `original` varchar(30) DEFAULT NULL,
		  `mankous` varchar(30) DEFAULT NULL,
		  `feminable` varchar(30) DEFAULT NULL,
		  `number` varchar(30) DEFAULT NULL,
		  `dualable` varchar(30) DEFAULT NULL,
		  `masculin_plural` varchar(30) DEFAULT NULL,
		  `feminin_plural` varchar(30) DEFAULT NULL,
		  `broken_plural` varchar(30) DEFAULT NULL,
		  `mamnou3_sarf` varchar(30) DEFAULT NULL,
		  `relative` varchar(30) DEFAULT NULL,
		  `w_suffix` varchar(30) DEFAULT NULL,
		  `hm_suffix` varchar(30) DEFAULT NULL,
		  `kal_prefix` varchar(30) DEFAULT NULL,
		  `ha_suffix` varchar(30) DEFAULT NULL,
		  `k_suffix` varchar(30) DEFAULT NULL,
		  `annex` varchar(30) DEFAULT NULL,
		  `definition` text,
		  `note` text
		)  DEFAULT CHARSET=utf8;
```
###XML format 

```xml
<?xml version='1.0' encoding='utf8'?>
<dictionary>
<noun>
	<vocalized>أعسر</vocalized> 
	<unvocalized>أعسر</unvocalized>
	 <wordtype>اسم تفضيل</wordtype> 
	 <root></root> <original></original> 
	 <mankous></mankous>
	 <feminable></feminable> 
	 <number>جمع تكسير</number> 
	 <dualable>DnN</dualable> 
	 <masculin_plural>Pm</masculin_plural> 
	 <feminin_plural></feminin_plural> 
	 <broken_plural>""</broken_plural> 
	 <mamnou3_sarf>ممنوع من الصرف</mamnou3_sarf>
	 <relative></relative>
	 <w_suffix></w_suffix> 
	 <hm_suffix></hm_suffix>
	 <kal_prefix></kal_prefix>
	 <ha_suffix></ha_suffix>
	 <k_suffix></k_suffix> 
	 <annex></annex> <definition>
	 </definition> <note>:لا جذر:لا مفرد:لا تشكيل:لا شرح</note>
 </noun>
....
</dictionary>
```

##Script Files:

1- generate the abstract dictionary from the brut manual dictionary:
```shell
generateverbdict.py -f data/verb_dic_data-net.csv > output/verbs.aya.dic
```

2- conjugate the verbs in the abstract dictionary to hunspell format
```shell
	conjugateToSpell.py -f data/verb_dic_data-net.csv > output/verbs.aya.dic
  ```


3- spellverbconst.py : constants used in the generation process
4- spellverb.py	     : basic functions used in the generation process

5- spelltools.py	: a script used to convert numeric flags into letters flags, especially for tools	


* [libqutrub]:
	* the Qutrub conjugator used to generate verbs forms.
* [docs]
	* documentation
* [data]
	* data files
* [output]
	* output files 
* [tools]
	* some scripts used to test.





Data Files:
=============
This files are used to create ayaspell dictionary for spellchecking
arramooz\verbs\data


File|Description
----|-----------
verb_dic_data-net.csv | 	brut data made manually by Mohamed kebdani.
ar_verb_normalized.dict|	A list of arabic verbs, from Qutrub project.
triverbtable.py		|		A list of trilateral verbs, used by Qutrub.
verbs.aya.dic 		|		The verb dictionary in abstract format.
verb.huns.dic			|	The Hunspell format of verb dictionary generated by using qutrub verb conjugator.



