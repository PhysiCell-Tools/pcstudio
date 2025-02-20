# cp ~/git/PhysiCell_rheiland_dev-9-11-24/BioFVM/* BioFVM/
# cp ~/git/PhysiCell_rheiland_dev-9-11-24/core/* core/
# cp ~/git/PhysiCell_rheiland_dev-9-11-24/modules/* modules/

# from the /src dir
cp ~/dev/PhysiCell-1.14.2/VERSION.txt .
cp ~/dev/PhysiCell-1.14.2/changes.md .
cp ~/dev/PhysiCell-1.14.2/beta/* beta/

cp ~/dev/PhysiCell-1.14.2/licenses/* licenses/

cp -R ~/dev/PhysiCell-1.14.2/addons .
cp -R ~/dev/PhysiCell-1.14.2/sample_projects .
cp -R ~/dev/PhysiCell-1.14.2/sample_projects_intracellular .

cp ~/dev/PhysiCell-1.14.2/BioFVM/* BioFVM/
cp ~/dev/PhysiCell-1.14.2/core/* core/
cp ~/dev/PhysiCell-1.14.2/modules/* modules/

cp ~/dev/PhysiCell-1.14.2/sample_projects/template/main.cpp .

cp ~/dev/PhysiCell-1.14.2/sample_projects/template/custom_modules/custom.cpp custom_modules/custom.cpp 
cp ~/dev/PhysiCell-1.14.2/sample_projects/template/custom_modules/custom.h custom_modules/custom.h 

cp ~/dev/PhysiCell-1.14.2/sample_projects/biorobots/custom_modules/custom.cpp custom_modules/biorobots.cpp 
#-->
echo 'NB! --> edit biorobots.cpp to use #include "./biorobots.h"'
cp ~/dev/PhysiCell-1.14.2/sample_projects/biorobots/custom_modules/custom.h custom_modules/biorobots.h 

# # update the 2 sample models' executables
# (base) M1P~/git/pcstudio/src/custom_modules$ diff biorobots.cpp ~/git/mathcancer_dev-9-15-24/sample_projects/biorobots/custom_modules/custom.cpp
# (base) M1P~/git/pcstudio/src/custom_modules$ cp ~/git/mathcancer_dev-9-15-24/sample_projects/biorobots/custom_modules/custom.cpp biorobots.cpp
# (base) M1P~/git/pcstudio/src/custom_modules$ vi biorobots.cpp


# (base) M1P~/git/pcstudio/src/custom_modules$ diff custom.cpp ~/git/mathcancer_dev-9-15-24/sample_projects/template/custom_modules/custom.cpp
# (base) M1P~/git/pcstudio/src/custom_modules$ cp ~/git/mathcancer_dev-9-15-24/sample_projects/template/custom_modules/custom.cpp .


