# Arramooz
Arabic Dictionary for Morphological analysis

[![downloads]( https://img.shields.io/sourceforge/dt/arramooz.svg)](http://sourceforge.org/projects/arramooz)
[![downloads]( https://img.shields.io/sourceforge/dm/arramooz.svg)](http://sourceforge.org/projects/arramooz)

  Developers:  Taha Zerrouki: http://tahadz.com
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



## Data Structure 

Data Structures in multiple format (csv, sql, xml) are described in [DataStructures.md](docs/datastructures.md)

* nouns and verbs are described in datastructures.md
* Stop words ( are explained in separate project [Arabic Stopwords](http://github.com/linuxscout/arabicstopwords)

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



