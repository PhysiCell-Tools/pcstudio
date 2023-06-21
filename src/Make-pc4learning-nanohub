VERSION := $(shell grep . VERSION.txt | cut -f1 -d:)
PROGRAM_NAME0:= template
PROGRAM_NAME1:= biorobots
PROGRAM_NAME2:= celltypes3
PROGRAM_NAME3:= pred_prey
PROGRAM_NAME4:= interactions

osRelease = $(shell lsb_release -r | sed -e "s/Release:\W*//" -e "s/\..*//")
ifeq ($(osRelease),7)
	hostName = $(shell hostname | sed -e "s:[-_].*::")$(osRelease)
else
	hostName = $(shell hostname | sed -e "s:[-_].*::")
endif

ifeq ($(hostName),nanohub7)
	BIN = ../bin
	MODINIT = . /etc/environ.sh
	MODCMD = use -e -r anaconda3-5.1
else
ifeq ($(hostName),rice7)
	BIN = ../bin/rice7
	MODINIT = . $(MODULESHOME)/init/sh
	MODCMD = module purge 2> /dev/null; module load gcc/7.3.0
endif
ifeq ($(hostName),brown7)
	BIN = ../bin/brown7
	MODINIT = . $(MODULESHOME)/init/sh
	MODCMD = module purge 2> /dev/null; module load gcc/7.3.0
endif
endif

CC := g++
# CC := g++-mp-7 # typical macports compiler name
# CC := g++-7 # typical homebrew compiler name 

# Check for environment definitions of compiler 
# e.g., on CC = g++-7 on OSX
ifdef PHYSICELL_CPP 
	CC := $(PHYSICELL_CPP)
endif

ARCH := native # best auto-tuning
# ARCH := core2 # a reasonably safe default for most CPUs since 2007
# ARCH := corei7
# ARCH := corei7-avx # earlier i7 
# ARCH := core-avx-i # i7 ivy bridge or newer 
# ARCH := core-avx2 # i7 with Haswell or newer
# ARCH := nehalem
# ARCH := westmere
# ARCH := sandybridge # circa 2011
# ARCH := ivybridge   # circa 2012
# ARCH := haswell     # circa 2013
# ARCH := broadwell   # circa 2014
# ARCH := skylake     # circa 2015
# ARCH := bonnell
# ARCH := silvermont
# ARCH := skylake-avx512
# ARCH := nocona #64-bit pentium 4 or later 

# CFLAGS := -march=$(ARCH) -Ofast -s -fomit-frame-pointer -mfpmath=both -fopenmp -m64 -std=c++11
# remove the -march arg to avoid SIGILL error on nanoHUB
CFLAGS := -O3 -fomit-frame-pointer -mfpmath=both -fopenmp -m64 -std=c++11

#CFLAGS := -march=$(ARCH) -O3 -fomit-frame-pointer -mfpmath=both -fopenmp -m64 -std=c++11
ifeq ($(OS),Windows_NT)
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Darwin)
		UNAME_P := $(shell uname -p)
		var0 := $(shell which $(CC))
		var1 := $(shell file $(var0))
		var2 := $(lastword $(var1))
		ifeq "$(var2)" "arm64"
			CFLAGS := -march=$(ARCH) -O3 -fomit-frame-pointer -fopenmp -m64 -std=c++11
		endif
	endif
endif

COMPILE_COMMAND := $(CC) $(CFLAGS) 

BioFVM_OBJECTS := BioFVM_vector.o BioFVM_mesh.o BioFVM_microenvironment.o BioFVM_solvers.o BioFVM_matlab.o \
BioFVM_utilities.o BioFVM_basic_agent.o BioFVM_MultiCellDS.o BioFVM_agent_container.o 

PhysiCell_core_OBJECTS := PhysiCell_phenotype.o PhysiCell_cell_container.o PhysiCell_standard_models.o \
PhysiCell_cell.o PhysiCell_custom.o PhysiCell_utilities.o PhysiCell_constants.o PhysiCell_basic_signaling.o PhysiCell_signal_behavior.o

PhysiCell_module_OBJECTS := PhysiCell_SVG.o PhysiCell_pathology.o PhysiCell_MultiCellDS.o PhysiCell_various_outputs.o \
PhysiCell_pugixml.o PhysiCell_settings.o PhysiCell_geometry.o

# put your custom objects here (they should be in the custom_modules directory)

# biorobots_custom_module_OBJECTS := custom_biorobots.o 
# celltypes3_custom_module_OBJECTS := custom_celltypes3.o 
# pred_prey_custom_module_OBJECTS := pred_prey_farmer.o 

pugixml_OBJECTS := pugixml.o

PhysiCell_OBJECTS := $(BioFVM_OBJECTS)  $(pugixml_OBJECTS) $(PhysiCell_core_OBJECTS) $(PhysiCell_module_OBJECTS)
#ALL_OBJECTS1 := $(PhysiCell_OBJECTS) $(biorobots_custom_module_OBJECTS)
#ALL_OBJECTS2 := $(PhysiCell_OBJECTS) $(celltypes3_custom_module_OBJECTS)
ALL_OBJECTS0 := $(PhysiCell_OBJECTS) template.o
ALL_OBJECTS1 := $(PhysiCell_OBJECTS) biorobots.o
ALL_OBJECTS2 := $(PhysiCell_OBJECTS) celltypes3.o
ALL_OBJECTS3 := $(PhysiCell_OBJECTS) pred_prey_farmer.o
ALL_OBJECTS4 := $(PhysiCell_OBJECTS) interactions.o

# compile the project 

all: main-template.cpp $(ALL_OBJECTS0) $(ALL_OBJECTS1) $(ALL_OBJECTS2) $(ALL_OBJECTS3) $(ALL_OBJECTS4)
	$(COMPILE_COMMAND) -o $(PROGRAM_NAME0) $(ALL_OBJECTS0) main-template.cpp 
	$(COMPILE_COMMAND) -o $(PROGRAM_NAME1) $(ALL_OBJECTS1) main-biorobots.cpp 
	$(COMPILE_COMMAND) -o $(PROGRAM_NAME2) $(ALL_OBJECTS2) main-celltypes3.cpp 
	$(COMPILE_COMMAND) -o $(PROGRAM_NAME3) $(ALL_OBJECTS3) main-pred-prey-farmer.cpp 
	$(COMPILE_COMMAND) -o $(PROGRAM_NAME4) $(ALL_OBJECTS4) main-interactions.cpp 

# PhysiCell core components	

PhysiCell_phenotype.o: ./core/PhysiCell_phenotype.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_phenotype.cpp
	
PhysiCell_digital_cell_line.o: ./core/PhysiCell_digital_cell_line.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_digital_cell_line.cpp

PhysiCell_cell.o: ./core/PhysiCell_cell.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_cell.cpp 

PhysiCell_cell_container.o: ./core/PhysiCell_cell_container.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_cell_container.cpp 
	
PhysiCell_standard_models.o: ./core/PhysiCell_standard_models.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_standard_models.cpp 
	
PhysiCell_utilities.o: ./core/PhysiCell_utilities.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_utilities.cpp 
	
PhysiCell_custom.o: ./core/PhysiCell_custom.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_custom.cpp 
	
PhysiCell_constants.o: ./core/PhysiCell_constants.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_constants.cpp 

PhysiCell_signal_behavior.o: ./core/PhysiCell_signal_behavior.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_signal_behavior.cpp 
	
# BioFVM core components (needed by PhysiCell)
	
BioFVM_vector.o: ./BioFVM/BioFVM_vector.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_vector.cpp 

BioFVM_agent_container.o: ./BioFVM/BioFVM_agent_container.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_agent_container.cpp 
	
BioFVM_mesh.o: ./BioFVM/BioFVM_mesh.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_mesh.cpp 

BioFVM_microenvironment.o: ./BioFVM/BioFVM_microenvironment.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_microenvironment.cpp 

BioFVM_solvers.o: ./BioFVM/BioFVM_solvers.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_solvers.cpp 

BioFVM_utilities.o: ./BioFVM/BioFVM_utilities.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_utilities.cpp 
	
BioFVM_basic_agent.o: ./BioFVM/BioFVM_basic_agent.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_basic_agent.cpp 
	
BioFVM_matlab.o: ./BioFVM/BioFVM_matlab.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_matlab.cpp

BioFVM_MultiCellDS.o: ./BioFVM/BioFVM_MultiCellDS.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/BioFVM_MultiCellDS.cpp
	
pugixml.o: ./BioFVM/pugixml.cpp
	$(COMPILE_COMMAND) -c ./BioFVM/pugixml.cpp
	
# standard PhysiCell modules

PhysiCell_SVG.o: ./modules/PhysiCell_SVG.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_SVG.cpp

PhysiCell_pathology.o: ./modules/PhysiCell_pathology.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_pathology.cpp

PhysiCell_MultiCellDS.o: ./modules/PhysiCell_MultiCellDS.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_MultiCellDS.cpp

PhysiCell_various_outputs.o: ./modules/PhysiCell_various_outputs.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_various_outputs.cpp

PhysiCell_pugixml.o: ./modules/PhysiCell_pugixml.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_pugixml.cpp
	
PhysiCell_settings.o: ./modules/PhysiCell_settings.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_settings.cpp
	
PhysiCell_basic_signaling.o: ./core/PhysiCell_basic_signaling.cpp
	$(COMPILE_COMMAND) -c ./core/PhysiCell_basic_signaling.cpp 	
	
PhysiCell_geometry.o: ./modules/PhysiCell_geometry.cpp
	$(COMPILE_COMMAND) -c ./modules/PhysiCell_geometry.cpp 
	
# user-defined PhysiCell modules

template.o: ./custom_modules/template.cpp 
	$(COMPILE_COMMAND) -c ./custom_modules/template.cpp
biorobots.o: ./custom_modules/biorobots.cpp 
	$(COMPILE_COMMAND) -c ./custom_modules/biorobots.cpp
celltypes3.o: ./custom_modules/celltypes3.cpp 
	$(COMPILE_COMMAND) -c ./custom_modules/celltypes3.cpp
pred_prey_farmer.o: ./custom_modules/pred_prey_farmer.cpp 
	$(COMPILE_COMMAND) -c ./custom_modules/pred_prey_farmer.cpp
interactions.o: ./custom_modules/interactions.cpp 
	$(COMPILE_COMMAND) -c ./custom_modules/interactions.cpp

	
# next targets for nanoHUB
install: 
	$(MODINIT); $(MODCMD); make all
	install --mode 0755 -D $(PROGRAM_NAME0) $(BIN)/$(PROGRAM_NAME0)
	install --mode 0755 -D $(PROGRAM_NAME1) $(BIN)/$(PROGRAM_NAME1)
	install --mode 0755 -D $(PROGRAM_NAME2) $(BIN)/$(PROGRAM_NAME2)
	install --mode 0755 -D $(PROGRAM_NAME3) $(BIN)/$(PROGRAM_NAME3)
	install --mode 0755 -D $(PROGRAM_NAME4) $(BIN)/$(PROGRAM_NAME4)

distclean: clean
	rm -f $(BIN)/$(PROGRAM_NAME0)
	rm -f $(BIN)/$(PROGRAM_NAME1)
	rm -f $(BIN)/$(PROGRAM_NAME2)
	rm -f $(BIN)/$(PROGRAM_NAME3)
	rm -f $(BIN)/$(PROGRAM_NAME4)
	rm -rf $(BIN)/__pycache__
	rm -rf ../.ipynb_checkpoints

clean:
	rm -f *.o
	rm -f $(PROGRAM_NAME0)
	rm -f $(PROGRAM_NAME1)
	rm -f $(PROGRAM_NAME2)
	rm -f $(PROGRAM_NAME3)
	rm -f $(PROGRAM_NAME4)
	
data-cleanup:
	rm -rf ./output
	mkdir ./output
	touch ./output/empty.txt
	
# archival 
	
checkpoint: 
	zip -r $$(date +%b_%d_%Y_%H%M).zip Makefile *.cpp *.h config/*.xml custom_modules/* 
	
zip:
	zip -r latest.zip Makefile* *.cpp *.h BioFVM/* config/* core/* custom_modules/* matlab/* modules/* sample_projects/* 
	cp latest.zip $$(date +%b_%d_%Y_%H%M).zip
	cp latest.zip VERSION_$(VERSION).zip 
	mv *.zip archives/
	
tar:
	tar --ignore-failed-read -czf latest.tar Makefile* *.cpp *.h BioFVM/* config/* core/* custom_modules/* matlab/* modules/* sample_projects/* 
	cp latest.tar $$(date +%b_%d_%Y_%H%M).tar
	cp latest.tar VERSION_$(VERSION).tar
	mv *.tar archives/

unzip: 
	cp ./archives/latest.zip . 
	unzip latest.zip 
	
untar: 
	cp ./archives/latest.tar .
	tar -xzf latest.tar

# easier animation 

FRAMERATE := 24
OUTPUT := output

jpeg: 
	@magick identify -format "%h" $(OUTPUT)/initial.svg >> __H.txt 
	@magick identify -format "%w" $(OUTPUT)/initial.svg >> __W.txt 
	@expr 2 \* \( $$(grep . __H.txt) / 2 \) >> __H1.txt 
	@expr 2 \* \( $$(grep . __W.txt) / 2 \) >> __W1.txt 
	@echo "$$(grep . __W1.txt)!x$$(grep . __H1.txt)!" >> __resize.txt 
	@magick mogrify -format jpg -resize $$(grep . __resize.txt) $(OUTPUT)/s*.svg
	rm -f __H*.txt __W*.txt __resize.txt 
	
gif: 
	magick convert $(OUTPUT)/s*.svg $(OUTPUT)/out.gif 
	 
movie:
	ffmpeg -r $(FRAMERATE) -f image2 -i $(OUTPUT)/snapshot%08d.jpg -vcodec libx264 -pix_fmt yuv420p -strict -2 -tune animation -crf 15 -acodec none $(OUTPUT)/out.mp4
	