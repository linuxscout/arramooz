#/usr/bin/sh
# Build Arramooz dictionary files
DATA_DIR :=data
RELEASES :=releases
OUTPUT :=output
SCRIPT :=scripts
VERSION=0.4.1
DOC="."

default: all
# Clean build files
clean:
	rm -f -r $(RELEASES)/* $(OUTPUT)
backup: 
	mkdir -p $(RELEASES)/backup$(VERSION)
	touch $(RELEASES)/todo.bz2
	mv $(RELEASES)/*.bz2 $(RELEASES)/backup$(VERSION)
#create all files 
all: ods verb noun release

# Publish to github
publish:
	git push origin master 

ods: verbods nounods
#Generate csv files from ODS
	mkdir -p $(OUTPUT)
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
	python3 $(SCRIPT)/verbs/gen_verb_dict.py -f $(DATA_DIR)/verbs/verb_dic_data-net.csv -t $(DATA_DIR)/verbs/verb_triliteral.csv> $(OUTPUT)/verbs.aya.dic
verbxml:
	#Generate Specific format SQL and XML
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o xml  --header -l 100 -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.xml
verbsql:

	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o sql  --header -v $(VERSION)  -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_v_voc' ON 'verbs' ('vocalized' ASC);" >> $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx__verbstamp' ON 'verbs' ('stamped' ASC);" >> $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_verb_norm'  ON 'verbs' ('normalized' ASC);" >> $(OUTPUT)/verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_verb_unvoc' ON 'verbs' ('unvocalized' ASC);" >> $(OUTPUT)/verbs.sql
verbcsv:
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o csv  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.csv
verbcheck:
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o check  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.check.csv

spell: verbspell nounspell
	#gerenate spelling dict in Hunspell format
verbspell:
	#gerenate spelling dict of verbs in Hunspell format
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o spell  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.spell
	python3 $(SCRIPT)/verbs/spelltools.py -f $(OUTPUT)/verbs.spell > $(OUTPUT)/verbs.2.spell
verbtags: verbdict
	#gerenate verb tags format
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o tags  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.tags

verbtagstest: verbdict
	#gerenate verb tags format
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -l 100 -o tags  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.test.tags
nountagstest:
	#gerenate spelling dict of nouns in Hunspell format
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -l 100 -f $(DATA_DIR)/nouns/fa3il.csv -d tags -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.test.tags
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -l 100 -f $(DATA_DIR)/nouns/maf3oul.csv -d tags  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.test.tags
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -l 100 -f $(DATA_DIR)/nouns/jamid.csv -d tags  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.test.tags
	## mansoub.csv
nountags:
	#gerenate spelling dict of nouns in Hunspell format
	python3 $(SCRIPT)/nouns/gen_noun_dict.py   -f $(DATA_DIR)/nouns/fa3il.csv -d tags -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.tags
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d tags  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.tags
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d tags  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.tags
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d tags  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.tags
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d tags  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.tags
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d tags  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.tags
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d tags  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.tags
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d tags  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.tags
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d tags -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.tags
toolstags: 
	#gerenate verb tags format
	python3 $(SCRIPT)/tools/generate_jar.py > $(OUTPUT)/tools.tags
	cat $(DATA_DIR)/stopwords/numbers.csv >> $(OUTPUT)/tools.tags

tagset:
	#build the whole dictionary
	cat $(OUTPUT)/verbs.tags  $(OUTPUT)/tools.tags $(OUTPUT)/nouns.dict.tags > $(OUTPUT)/arabic.dic.tags 
	cut -f3  $(OUTPUT)/arabic.dic.tags > /tmp/arab_tags.txt
	sort -u /tmp/arab_tags.txt  > $(OUTPUT)/arabic_tags.txt

nounspell:
	#gerenate spelling dict of nouns in Hunspell format
	python3 $(SCRIPT)/nouns/gen_noun_dict.py   -f $(DATA_DIR)/nouns/fa3il.csv -d spell -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.spell
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d spell  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.spell
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d spell  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.spell
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d spell  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.spell
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d spell  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.spell
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d spell  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.spell
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d spell  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.spell
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d spell  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.spell
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d spell -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.spell
#~ 

nouncsv:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d txt  -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.csv
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d txt  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.csv
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d txt  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.csv
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d txt  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.csv
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d txt  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.csv
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d txt  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.csv
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d txt  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.csv
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d txt  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.csv
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d txt  -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.csv
nouncheck:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d check  -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.check.csv
#~ 	## maf3oul file
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d check  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## jamid file
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d check  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## mansoub.csv
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d check  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## masdar.csv
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d check  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## moubalagha.csv
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d check  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## mouchabbaha.csv
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d check  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## sifates.csv
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d check  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.check.csv
#~ 	## tafdil.csv
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d check  -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.check.csv
nounxml:
	# XML files generating 
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv  -v $(VERSION)  -t fa3il -d xml  >$(OUTPUT)/nouns.fa3il.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv  -v $(VERSION)  -d xml -t maf3oul >$(OUTPUT)/nouns.maf3oul.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv  -v $(VERSION)  -d xml -t jamid >$(OUTPUT)/nouns.jamid.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv  -v $(VERSION) -d xml -t mansoub >$(OUTPUT)/nouns.mansoub.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv  -v $(VERSION)  -d xml -t masdar >$(OUTPUT)/nouns.masdar.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv  -v $(VERSION)  -d xml -t moubalagha >$(OUTPUT)/nouns.moubalagha.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv  -v $(VERSION) -d xml -t mouchabbaha >$(OUTPUT)/nouns.mouchabbaha.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv  -v $(VERSION)  -d xml -t sifates  >$(OUTPUT)/nouns.sifates.dict.xml
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv   -v $(VERSION)  -d xml -t tafdil >$(OUTPUT)/nouns.tafdil.dict.xml

nounsql:
	############ SQL files generation
	# fa3il file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  --header -f $(DATA_DIR)/nouns/fa3il.csv  -v $(VERSION) -d sql -t fa3il  >$(OUTPUT)/nouns.dict.sql
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv  -v $(VERSION) -d sql -t maf3oul >>$(OUTPUT)/nouns.dict.sql
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv  -v $(VERSION) -d sql -t jamid >>$(OUTPUT)/nouns.dict.sql
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv  -v $(VERSION) -d sql -t mansoub >>$(OUTPUT)/nouns.dict.sql
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv  -v $(VERSION) -d sql -t masdar >>$(OUTPUT)/nouns.dict.sql
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv  -v $(VERSION) -d sql -t moubalagha >>$(OUTPUT)/nouns.dict.sql
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv  -v $(VERSION) -d sql -t mouchabbaha >>$(OUTPUT)/nouns.dict.sql
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv  -v $(VERSION) -d sql -t sifates  >>$(OUTPUT)/nouns.dict.sql
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv   -v $(VERSION) -d sql -t tafdil >>$(OUTPUT)/nouns.dict.sql
	
	echo "CREATE INDEX IF NOT EXISTS 'idx_n_voc'  ON 'nouns' ('vocalized' ASC);"   >>$(OUTPUT)/nouns.dict.sql
	echo "CREATE INDEX IF NOT EXISTS 'idx_norm_n' ON 'nouns' ('normalized' ASC);" >>$(OUTPUT)/nouns.dict.sql
	echo "CREATE INDEX IF NOT EXISTS 'idx_stamp'  ON 'nouns' ('stamped' ASC);"		  >>$(OUTPUT)/nouns.dict.sql
	echo "CREATE INDEX IF NOT EXISTS 'idx_unv'    ON 'nouns' ('unvocalized' ASC);"   >>$(OUTPUT)/nouns.dict.sql



nounstardict:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d stardict  -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.sdic
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d stardict  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.sdic
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d stardict  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.sdic
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d stardict  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.sdic
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d stardict  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.sdic
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d stardict  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.sdic
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d stardict  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.sdic
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d stardict  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.sdic
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d stardict -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.sdic
	#~ sed -i "s/\n\n\n/\n\n/g" $(OUTPUT)/nouns.dict.sdic
	#~ sed -i "s/\n\n\n/\n\n/g" $(OUTPUT)/nouns.dict.sdic
verbstardict:
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o stardict  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.sdic
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
sqlite:
	# csv
	mkdir -p $(RELEASES)/sqlite/
	
#~ 	mv $(RELEASES)/sqlite/arabicdictionary.sqlite  $(RELEASES)/sqlite/arabicdictionary.sqlite.old
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite < $(OUTPUT)/nouns.dict.sql
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite < $(OUTPUT)/verbs.sql
	# create index
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx_vunv ON verbs (unvocalized ASC);"
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx_vnorm ON verbs (normalized ASC);"
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx__vstamp ON verbs (stamped ASC);"
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx_nvoc ON nouns (vocalized ASC);"
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx_nunv ON nouns (unvocalized ASC);"
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx_nnorm ON nouns (normalized ASC);"
	sqlite3  $(RELEASES)/sqlite/arabicdictionary.sqlite "CREATE INDEX idx_nstamp ON nouns (stamped ASC);"


# create customized dictionay in order to add new entries easly
custom: cust_ods cust_verb cust_noun cust_sqlite
cust_ods:
	libreoffice --headless --convert-to "csv:Text - txt - csv (StarCalc):9,34,UTF8" --outdir $(DATA_DIR)/custom/ $(DATA_DIR)/custom/*.ods

cust_noun:
	############ SQL files generation
	# fa3il file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/custom/nouns.csv  -v $(VERSION) -d sql -t custom  >$(OUTPUT)/custom_nouns.dict.sql
	
cust_verb:
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o sql  -v $(VERSION)  -f $(DATA_DIR)/custom/verbs.aya.csv > $(OUTPUT)/custom_verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_v_voc' ON 'verbs' ('vocalized' ASC);" >> $(OUTPUT)/custom_verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx__verbstamp' ON 'verbs' ('stamped' ASC);" >> $(OUTPUT)/custom_verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_verb_norm'  ON 'verbs' ('normalized' ASC);" >> $(OUTPUT)/custom_verbs.sql
	echo "CREATE INDEX  IF NOT EXISTS 'idx_verb_unvoc' ON 'verbs' ('unvocalized' ASC);" >> $(OUTPUT)/custom_verbs.sql
cust_sqlite:
	# sqlite
	mkdir -p $(RELEASES)/sqlite/
	mv $(RELEASES)/sqlite/custom_dictionary.sqlite  $(RELEASES)/sqlite/custom_dictionary.sqlite.old
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite < $(OUTPUT)/custom_nouns.dict.sql
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite < $(OUTPUT)/custom_verbs.sql
	# create index
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx_vunv ON verbs (unvocalized ASC);"
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx_vnorm ON verbs (normalized ASC);"
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx__vstamp ON verbs (stamped ASC);"
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx_nvoc ON nouns (vocalized ASC);"
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx_nunv ON nouns (unvocalized ASC);"
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx_nnorm ON nouns (normalized ASC);"
	sqlite3  $(RELEASES)/sqlite/custom_dictionary.sqlite "CREATE INDEX idx_nstamp ON nouns (stamped ASC);"


taksir:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d taksir --header -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.taksir.csv
	## maf3oul file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d taksir  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.taksir.csv
	## jamid file
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d taksir  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.taksir.csv
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d taksir  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.taksir.csv
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d taksir  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.taksir.csv
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d taksir  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.taksir.csv
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d taksir  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.taksir.csv
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d taksir  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.taksir.csv
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d taksir  -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.taksir.csv

nounwordlist:
	#gerenate vocalized wordlist dict of nouns in csv format
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py   -f $(DATA_DIR)/nouns/fa3il.csv -d wordlist -v $(VERSION) -t fa3il >$(OUTPUT)/fa3il.dict.wordlist
#~ 	## maf3oul file
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d wordlist  -v $(VERSION) -t maf3oul >$(OUTPUT)/maf3oul.dict.wordlist
#~ 	## jamid file
#~ 	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d wordlist  -v $(VERSION) -t jamid >$(OUTPUT)/jamid.dict.wordlist
	## mansoub.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d wordlist  -v $(VERSION) -t mansoub >$(OUTPUT)/mansoub.dict.wordlist
	## masdar.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d wordlist  -v $(VERSION) -t masdar >$(OUTPUT)/masdar.dict.wordlist
	## moubalagha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d wordlist  -v $(VERSION) -t moubalagha >$(OUTPUT)/moubalagha.dict.wordlist
	## mouchabbaha.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d wordlist  -v $(VERSION) -t mouchabbaha >$(OUTPUT)/mouchabbaha.dict.wordlist
	## sifates.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d wordlist  -v $(VERSION) -t sifates  >$(OUTPUT)/sifates.dict.wordlist
	## tafdil.csv
	python3 $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d wordlist -v $(VERSION) -t tafdil >$(OUTPUT)/tafdil.dict.wordlist
verbwordlist: verbdict
	#gerenate verb tags format
	python3 $(SCRIPT)/verbs/gen_verb_dict_format.py -o wordlist  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.wordlist
