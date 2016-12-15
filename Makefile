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
release: xmlpack sqlpack csvpack
verb: verbods verbdict  verbcsv verbxml verbsql
noun: nounods nouncsv nounxml nounsql 
verbdict:
	#Generate verb dictionary
	python $(SCRIPT)/verbs/gen_verb_dict.py -f $(DATA_DIR)/verbs/verb_dic_data-net.csv > $(OUTPUT)/verbs.aya.dic
verbxml:
	#Generate Specific format SQL and XML
	python $(SCRIPT)/verbs/gen_verb_dict_format.py -o xml -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.xml
verbsql:
	python $(SCRIPT)/verbs/gen_verb_dict_format.py -o sql  -v $(VERSION)  -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.sql
verbcsv:
	python $(SCRIPT)/verbs/gen_verb_dict_format.py -o csv  -v $(VERSION) -f $(OUTPUT)/verbs.aya.dic > $(OUTPUT)/verbs.csv

nouncsv:
	#Generate noun dictionary 
	# create a dictionary file from ayaspell cvs form
	# fa3il file
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv -d txt  -v $(VERSION) -t fa3il >$(OUTPUT)/nouns.dict.csv
	## maf3oul file
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv -d txt  -v $(VERSION) -t maf3oul >>$(OUTPUT)/nouns.dict.csv
	## jamid file
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv -d txt  -v $(VERSION) -t jamid >>$(OUTPUT)/nouns.dict.csv
	## mansoub.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv -d txt  -v $(VERSION) -t mansoub >>$(OUTPUT)/nouns.dict.csv
	## masdar.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv -d txt  -v $(VERSION) -t masdar >>$(OUTPUT)/nouns.dict.csv
	## moubalagha.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv -d txt  -v $(VERSION) -t moubalagha >>$(OUTPUT)/nouns.dict.csv
	## mouchabbaha.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv -d txt  -v $(VERSION) -t mouchabbaha >>$(OUTPUT)/nouns.dict.csv
	## sifates.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv -d txt  -v $(VERSION) -t sifates  >>$(OUTPUT)/nouns.dict.csv
	## tafdil.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv  -d txt  -v $(VERSION) -t tafdil >>$(OUTPUT)/nouns.dict.csv

nounxml:
	# XML files generating 
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv  -v $(VERSION)  -t fa3il -d xml  >$(OUTPUT)/nouns.fa3il.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv  -v $(VERSION)  -d xml -t maf3oul >$(OUTPUT)/nouns.maf3oul.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv  -v $(VERSION)  -d xml -t jamid >$(OUTPUT)/nouns.jamid.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv  -v $(VERSION) -d xml -t mansoub >$(OUTPUT)/nouns.mansoub.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv  -v $(VERSION)  -d xml -t masdar >$(OUTPUT)/nouns.masdar.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv  -v $(VERSION)  -d xml -t moubalagha >$(OUTPUT)/nouns.moubalagha.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv  -v $(VERSION) -d xml -t mouchabbaha >$(OUTPUT)/nouns.mouchabbaha.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv  -v $(VERSION)  -d xml -t sifates  >$(OUTPUT)/nouns.sifates.dict.xml
	python $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv   -v $(VERSION)  -d xml -t tafdil >$(OUTPUT)/nouns.tafdil.dict.xml

nounsql:
	############ SQL files generation
	# fa3il file
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/fa3il.csv  -v $(VERSION) -d sql -t fa3il  >$(OUTPUT)/nouns.dict.sql
	## maf3oul file
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/maf3oul.csv  -v $(VERSION) -d sql -t maf3oul >>$(OUTPUT)/nouns.dict.sql
	## jamid file
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/jamid.csv  -v $(VERSION) -d sql -t jamid >>$(OUTPUT)/nouns.dict.sql
	## mansoub.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mansoub.csv  -v $(VERSION) -d sql -t mansoub >>$(OUTPUT)/nouns.dict.sql
	## masdar.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/masdar.csv  -v $(VERSION) -d sql -t masdar >>$(OUTPUT)/nouns.dict.sql
	## moubalagha.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/moubalagha.csv  -v $(VERSION) -d sql -t moubalagha >>$(OUTPUT)/nouns.dict.sql
	## mouchabbaha.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py  -f $(DATA_DIR)/nouns/mouchabbaha.csv  -v $(VERSION) -d sql -t mouchabbaha >>$(OUTPUT)/nouns.dict.sql
	## sifates.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/sifates.csv  -v $(VERSION) -d sql -t sifates  >>$(OUTPUT)/nouns.dict.sql
	## tafdil.csv
	python $(SCRIPT)/nouns/gen_noun_dict.py -f $(DATA_DIR)/nouns/tafdil.csv   -v $(VERSION) -d sql -t tafdil >>$(OUTPUT)/nouns.dict.sql

#packaging 	
xmlpack:
	mkdir -p $(RELEASES)/xml/nouns

	cp $(OUTPUT)/nouns.*.dict.xml $(RELEASES)/xml/nouns
	cp $(OUTPUT)/verbs.xml $(RELEASES)/xml/
	cp $(DOC)/README.md $(RELEASES)/xml/
	cp $(DOC)/LICENSE $(RELEASES)/xml/
	cp $(DOC)/AUTHORS.md $(RELEASES)/xml/
	tar cfj $(RELEASES)/arramooz.xml.$(VERSION).tar.bz2 $(RELEASES)/xml/

sqlpack :
	# sql
	mkdir -p $(RELEASES)/sql
	cp $(OUTPUT)/nouns.dict.sql $(RELEASES)/sql/
	cp $(OUTPUT)/verbs.sql $(RELEASES)/sql/
	cp $(DOC)/README.md $(RELEASES)/sql/
	cp $(DOC)/LICENSE $(RELEASES)/sql/
	cp $(DOC)/AUTHORS.md $(RELEASES)/sql/
	tar cfj $(RELEASES)/arramooz.sql.$(VERSION).tar.bz2 $(RELEASES)/sql/

csvpack:
	# csv
	mkdir -p $(RELEASES)/csv/
	cp $(OUTPUT)/nouns.dict.csv $(RELEASES)/csv/
	cp $(OUTPUT)/verbs.csv $(RELEASES)/csv/
	cp $(DOC)/README.md $(RELEASES)/csv/
	cp $(DOC)/LICENSE $(RELEASES)/csv/
	cp $(DOC)/AUTHORS.md $(RELEASES)/csv/
	tar cfj $(RELEASES)/arramooz.csv.$(VERSION).tar.bz2 $(RELEASES)/csv/
