#/usr/bin/sh
# Build Arramooz dictionary files
DATA_DIR :=data
RELEASES :=releases
OUTPUT :=tests/output
SCRIPT :=scripts
VERSION=0.3
DOC="."

default: all
# Clean build files
clean:
	rm -f -r $(RELEASES)/*
backup: 
	mkdir -p $(RELEASES)/backup$(VERSION)
	mv $(RELEASES)/*.bz2 $(RELEASES)/backup$(VERSION)
#create all files 
all: ods verb noun release

# Publish to github
publish:
	git push origin master 

ods: verbods nounods
#Generate csv files from ODS
nounods:
	libreoffice --headless --convert-to "csv:Text - txt - csv (StarCalc):9,34,UTF8" --outdir $(DATA_DIR)/nouns/ $(DATA_DIR)/nouns/*.ods
verbods:
	libreoffice --headless --convert-to "csv:Text - txt - csv (StarCalc):9,34,UTF8" --outdir $(DATA_DIR)/verbs/ $(DATA_DIR)/verbs/*.ods
#Package files
release: backup xmlpack sqlpack csvpack
verb: verbods verbdict  verbcsv verbxml verbsql
noun: nounods nouncsv nounxml nounsql 
verbdict:
	#Generate verb dictionary
	mkdir -p $(OUTPUT)
	python2 $(SCRIPT)/verbs/gen_verb_dict.py -f $(DATA_DIR)/verbs/verb_dic_data-net.csv > $(OUTPUT)/verbs.aya.dic
verbxml:
	#Generate Specific format SQL and XML
	python2 $(SCRIPT)/verbs/gen_verb_dict_format.py -o xml -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.xml
verbsql:
	python2 $(SCRIPT)/verbs/gen_verb_dict_format.py -o sql  -v $(VERSION)  -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_v_voc' ON 'verbs' ('vocalized' ASC);" >> $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx__verbstamp' ON 'verbs' ('stamped' ASC);" >> $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_verb_norm'  ON 'verbs' ('normalized' ASC);" >> $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_verb_unvoc' ON 'verbs' ('unvocalized' ASC);" >> $(OUTPUT)/verbs.sql
verbcsv:
	python2 $(SCRIPT)/verbs/gen_verb_dict_format.py -o csv  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.csv

spell: verbspell nounspell
	#gerenate spelling dict in Hunspell format
verbspell:
	#gerenate spelling dict of verbs in Hunspell format
	python2 $(SCRIPT)/verbs/gen_verb_dict_format.py -o spell  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.spell
	python2 $(SCRIPT)/verbs/spelltools.py -f $(OUTPUT)/verbs.spell > $(OUTPUT)/verbs.2.spell

nounspelltest:
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -l 100  -f $(DATA_DIR)/nouns/fa3il.csv -d spell -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.spell
	## maf3oul file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -l 100 -f $(DATA_DIR)/nouns/maf3oul.csv -d spell  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.spell
	## jamid file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -l 100 -f $(DATA_DIR)/nouns/jamid.csv -d spell  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.spell
	## mansoub.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -l 100 -f $(DATA_DIR)/nouns/mansoub.csv -d spell  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.spell
	## masdar.csv
	
nounspell:
	#gerenate spelling dict of nouns in Hunspell format
	python2 $(SCRIPT)/nouns/gen_noun_dict.py   -f $(DATA_DIR)/nouns/fa3il.csv -d spell -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.spell
	## maf3oul file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d spell  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.spell
	## jamid file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d spell  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.spell
	## mansoub.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d spell  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.spell
	## masdar.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d spell  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.spell
	## moubalagha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d spell  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.spell
	## mouchabbaha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d spell  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.spell
	## sifates.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d spell  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.spell
	## tafdil.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d spell -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.spell
#~ 

nouncsv:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d txt  -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.csv
	## maf3oul file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d txt  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.csv
	## jamid file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d txt  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.csv
	## mansoub.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d txt  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.csv
	## masdar.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d txt  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.csv
	## moubalagha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d txt  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.csv
	## mouchabbaha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d txt  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.csv
	## sifates.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d txt  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.csv
	## tafdil.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d txt  -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.csv

nounxml:
	# XML files generating 
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv  -v $(VERSION)  -t fa3il -d xml  >$(OUTPUT)/nouns.fa3il.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv  -v $(VERSION)  -d xml -t maf3oul >$(OUTPUT)/nouns.maf3oul.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv  -v $(VERSION)  -d xml -t jamid >$(OUTPUT)/nouns.jamid.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv  -v $(VERSION) -d xml -t mansoub >$(OUTPUT)/nouns.mansoub.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv  -v $(VERSION)  -d xml -t masdar >$(OUTPUT)/nouns.masdar.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv  -v $(VERSION)  -d xml -t moubalagha >$(OUTPUT)/nouns.moubalagha.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv  -v $(VERSION) -d xml -t mouchabbaha >$(OUTPUT)/nouns.mouchabbaha.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv  -v $(VERSION)  -d xml -t sifates  >$(OUTPUT)/nouns.sifates.dict.xml
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv   -v $(VERSION)  -d xml -t tafdil >$(OUTPUT)/nouns.tafdil.dict.xml

nounsql:
	############ SQL files generation
	# fa3il file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv  -v $(VERSION) -d sql -t fa3il  >$(OUTPUT)/nouns.dict.sql
	## maf3oul file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv  -v $(VERSION) -d sql -t maf3oul >>$(OUTPUT)/nouns.dict.sql
	## jamid file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv  -v $(VERSION) -d sql -t jamid >>$(OUTPUT)/nouns.dict.sql
	## mansoub.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv  -v $(VERSION) -d sql -t mansoub >>$(OUTPUT)/nouns.dict.sql
	## masdar.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv  -v $(VERSION) -d sql -t masdar >>$(OUTPUT)/nouns.dict.sql
	## moubalagha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv  -v $(VERSION) -d sql -t moubalagha >>$(OUTPUT)/nouns.dict.sql
	## mouchabbaha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv  -v $(VERSION) -d sql -t mouchabbaha >>$(OUTPUT)/nouns.dict.sql
	## sifates.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv  -v $(VERSION) -d sql -t sifates  >>$(OUTPUT)/nouns.dict.sql
	## tafdil.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv   -v $(VERSION) -d sql -t tafdil >>$(OUTPUT)/nouns.dict.sql
	
	echo "CREATE INDEX IF NOT EXISTS 'idx_n_voc'  ON 'nouns' ('vocalized' ASC);"   >>$(OUTPUT)/nouns.dict.sql
	echo "CREATE INDEX IF NOT EXISTS 'idx_norm_n' ON 'nouns' ('normalized' ASC);" >>$(OUTPUT)/nouns.dict.sql
	echo "CREATE INDEX IF NOT EXISTS 'idx_stamp'  ON 'nouns' ('stamped' ASC);"		  >>$(OUTPUT)/nouns.dict.sql
	echo "CREATE INDEX IF NOT EXISTS 'idx_unv'    ON 'nouns' ('unvocalized' ASC);"   >>$(OUTPUT)/nouns.dict.sql



nounstardict:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d stardict  -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.sdic
	## maf3oul file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d stardict  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.sdic
	## jamid file
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d stardict  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.sdic
	## mansoub.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d stardict  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.sdic
	## masdar.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d stardict  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.sdic
	## moubalagha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d stardict  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.sdic
	## mouchabbaha.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d stardict  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.sdic
	## sifates.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d stardict  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.sdic
	## tafdil.csv
	python2 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d stardict -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.sdic
	#~ sed -i "s/\n\n\n/\n\n/g" $(OUTPUT)/nouns.dict.sdic
	#~ sed -i "s/\n\n\n/\n\n/g" $(OUTPUT)/nouns.dict.sdic
verbstardict:
	python2 $(SCRIPT)/verbs/gen_verb_dict_format.py -o stardict  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.sdic
	#~ sed -i "s/\n\n\n/\n\n/g" $(OUTPUT)/verbs.sdic
	#~ sed -i "s/\n\n\n/\n\n/g" $(OUTPUT)/verbs.sdic
#packaging 

xmlpack:
	mkdir -p $(RELEASES)/xml/nouns

	cp $(OUTPUT)/nouns.*.dict.xml $(RELEASES)/xml/nouns
	cp $(OUTPUT)/verbs.xml $(RELEASES)/xml/
	cp $(DOC)/README.md $(RELEASES)/xml/
	cp $(DOC)/LICENSE $(RELEASES)/xml/
	cp $(DOC)/AUTHORS.md $(RELEASES)/xml/
	cd $(RELEASES) && tar cfj arramooz.xml.$(VERSION).tar.bz2 xml/

sqlpack :
	# sql
	mkdir -p $(RELEASES)/sql
	cp $(OUTPUT)/nouns.dict.sql $(RELEASES)/sql/
	cp $(OUTPUT)/verbs.sql $(RELEASES)/sql/
	cp $(DOC)/README.md $(RELEASES)/sql/
	cp $(DOC)/LICENSE $(RELEASES)/sql/
	cp $(DOC)/AUTHORS.md $(RELEASES)/sql/
	cd $(RELEASES) && tar cfj arramooz.sql.$(VERSION).tar.bz2 sql/

csvpack:
	# csv
	mkdir -p $(RELEASES)/csv/
	cp $(OUTPUT)/nouns.dict.csv $(RELEASES)/csv/
	cp $(OUTPUT)/verbs.csv $(RELEASES)/csv/
	cp $(DOC)/README.md $(RELEASES)/csv/
	cp $(DOC)/LICENSE $(RELEASES)/csv/
	cp $(DOC)/AUTHORS.md $(RELEASES)/csv/
	cd $(RELEASES) && tar cfj arramooz.csv.$(VERSION).tar.bz2 csv/


stardictpack: nounstardict  verbstardict
	# stardict
	touch $(OUTPUT)/arramooz.sdic	
	echo "\n#version=2.4.2" >$(OUTPUT)/arramooz.sdic	
	echo "#bookname=Arramooz" >>$(OUTPUT)/arramooz.sdic
	echo "#sametypesequence=m" >>$(OUTPUT)/arramooz.sdic
	echo "#author=Taha Zerrouki" >>$(OUTPUT)/arramooz.sdic
	echo "#email=taha.zerrouki@gmail.com" >>$(OUTPUT)/arramooz.sdic
	echo "#website=http://arramooz.sf.net" >>$(OUTPUT)/arramooz.sdic
	echo "#description=Arrammoz arabic Dictionary converted to StarDict format" >>$(OUTPUT)/arramooz.sdic
	echo "#date=2016.12.16\n" >>$(OUTPUT)/arramooz.sdic

	cat $(OUTPUT)/nouns.dict.sdic $(OUTPUT)/verbs.sdic >> $(OUTPUT)/arramooz.sdic

	sed -i "s/\n\n(\n)+/\n\n/g" $(OUTPUT)/arramooz.sdic
	
	mkdir -p $(RELEASES)/stardict/
	cp $(OUTPUT)/arramooz.sdic $(RELEASES)/stardict/
	cp $(DOC)/README.md $(RELEASES)/stardict/
	cp $(DOC)/LICENSE $(RELEASES)/stardict/
	cp $(DOC)/AUTHORS.md $(RELEASES)/stardict/
	echo "*********************************************************************"
	echo "NOTE: you must use stardict-editor to Compile $(RELEASES)/stardict/arramooz.sdic"
	echo "*********************************************************************"	
