# cp ~/git/PhysiCell_rheiland_dev-9-11-24/BioFVM/* BioFVM/
# cp ~/git/PhysiCell_rheiland_dev-9-11-24/core/* core/
# cp ~/git/PhysiCell_rheiland_dev-9-11-24/modules/* modules/

cp ~/git/mathcancer_dev-9-15-24/BioFVM/* BioFVM/
cp ~/git/mathcancer_dev-9-15-24/core/* core/
cp ~/git/mathcancer_dev-9-15-24/modules/* modules/

cp ~/git/mathcancer_dev-9-15-24/sample_projects/template/main.cpp .

# update the 2 sample models' executables
(base) M1P~/git/pcstudio/src/custom_modules$ diff biorobots.cpp ~/git/mathcancer_dev-9-15-24/sample_projects/biorobots/custom_modules/custom.cpp
(base) M1P~/git/pcstudio/src/custom_modules$ cp ~/git/mathcancer_dev-9-15-24/sample_projects/biorobots/custom_modules/custom.cpp biorobots.cpp
(base) M1P~/git/pcstudio/src/custom_modules$ vi biorobots.cpp
-->
#include "./biorobots.h"


(base) M1P~/git/pcstudio/src/custom_modules$ diff custom.cpp ~/git/mathcancer_dev-9-15-24/sample_projects/template/custom_modules/custom.cpp
(base) M1P~/git/pcstudio/src/custom_modules$ cp ~/git/mathcancer_dev-9-15-24/sample_projects/template/custom_modules/custom.cpp .

