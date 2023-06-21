/*
###############################################################################
# If you use PhysiCell in your project, please cite PhysiCell and the version #
# number, such as below:                                                      #
#                                                                             #
# We implemented and solved the model using PhysiCell (Version x.y.z) [1].    #
#                                                                             #
# [1] A Ghaffarizadeh, R Heiland, SH Friedman, SM Mumenthaler, and P Macklin, #
#     PhysiCell: an Open Source Physics-Based Cell Simulator for Multicellu-  #
#     lar Systems, PLoS Comput. Biol. 14(2): e1005991, 2018                   #
#     DOI: 10.1371/journal.pcbi.1005991                                       #
#                                                                             #
# See VERSION.txt or call get_PhysiCell_version() to get the current version  #
#     x.y.z. Call display_citations() to get detailed information on all cite-#
#     able software used in your PhysiCell application.                       #
#                                                                             #
# Because PhysiCell extensively uses BioFVM, we suggest you also cite BioFVM  #
#     as below:                                                               #
#                                                                             #
# We implemented and solved the model using PhysiCell (Version x.y.z) [1],    #
# with BioFVM [2] to solve the transport equations.                           #
#                                                                             #
# [1] A Ghaffarizadeh, R Heiland, SH Friedman, SM Mumenthaler, and P Macklin, #
#     PhysiCell: an Open Source Physics-Based Cell Simulator for Multicellu-  #
#     lar Systems, PLoS Comput. Biol. 14(2): e1005991, 2018                   #
#     DOI: 10.1371/journal.pcbi.1005991                                       #
#                                                                             #
# [2] A Ghaffarizadeh, SH Friedman, and P Macklin, BioFVM: an efficient para- #
#     llelized diffusive transport solver for 3-D biological simulations,     #
#     Bioinformatics 32(8): 1256-8, 2016. DOI: 10.1093/bioinformatics/btv730  #
#                                                                             #
###############################################################################
#                                                                             #
# BSD 3-Clause License (see https://opensource.org/licenses/BSD-3-Clause)     #
#                                                                             #
# Copyright (c) 2015-2021, Paul Macklin and the PhysiCell Project             #
# All rights reserved.                                                        #
#                                                                             #
# Redistribution and use in source and binary forms, with or without          #
# modification, are permitted provided that the following conditions are met: #
#                                                                             #
# 1. Redistributions of source code must retain the above copyright notice,   #
# this list of conditions and the following disclaimer.                       #
#                                                                             #
# 2. Redistributions in binary form must reproduce the above copyright        #
# notice, this list of conditions and the following disclaimer in the         #
# documentation and/or other materials provided with the distribution.        #
#                                                                             #
# 3. Neither the name of the copyright holder nor the names of its            #
# contributors may be used to endorse or promote products derived from this   #
# software without specific prior written permission.                         #
#                                                                             #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE   #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE   #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR         #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF        #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS    #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN     #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)     #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  #
# POSSIBILITY OF SUCH DAMAGE.                                                 #
#                                                                             #
###############################################################################
*/

#include "../core/PhysiCell.h"
#include "../modules/PhysiCell_standard_modules.h" 


#include <typeinfo>


using namespace BioFVM; 
using namespace PhysiCell;

// setup functions to help us along 

void create_cell_types( void );
void setup_tissue( void ); 

// set up the BioFVM microenvironment 
void setup_microenvironment( void ); 

// custom pathology coloring function 

std::vector<std::string> my_coloring_function( Cell* );

// custom functions can go here 

void phenotype_function( Cell* pCell, Phenotype& phenotype, double dt );
void custom_function( Cell* pCell, Phenotype& phenotype , double dt );

void contact_function( Cell* pMe, Phenotype& phenoMe , Cell* pOther, Phenotype& phenoOther , double dt ); 


double extended_Hill_response_function( std::vector<double> signals, std::vector<double> half_maxes , std::vector<double> hill_powers ); 

class Hypothesis_Rule
{
 private:
    std::unordered_map<std::string,int> signals_map;  
 public:
    std::string cell_type; 
    Cell_Definition* pCell_Definition; 

    std::string behavior; 
    double base_value; 
    double max_value; 
    double min_value; 

    std::vector< std::string > signals; 
    std::vector<bool> responses; 
    std::vector<double> half_maxes; 
    std::vector<double> hill_powers; 

    std::vector< std::string > up_signals; 
    std::vector<double> up_half_maxes; 
    std::vector<double> up_hill_powers; 

    std::vector< std::string > down_signals; 
    std::vector<double> down_half_maxes; 
    std::vector<double> down_hill_powers; 

    Hypothesis_Rule(); // done 

    void sync_to_cell_definition( Cell_Definition* pCD ); // done 
    void sync_to_cell_definition( std::string cell_name ); // done 

    void add_signal( std::string signal , double half_max , double hill_power , std::string response ); // done 
    void add_signal( std::string signal , std::string response ); // done 

    double evaluate( std::vector<double> signal_values ); // done 
    double evaluate( Cell* pCell ); // done 
    void apply( Cell* pCell ); // done 

    int find_signal( std::string name ); // done 

    void set_half_max( std::string , double hm ); // done 
    void set_hill_power( std::string , double hp ); // done 
    void set_response( std::string , std::string response ); // done 

    void reduced_display( std::ostream& os ); // done 
    void display( std::ostream& os ); // done 
    void detailed_display( std::ostream& os ); // done 
}; 

class Hypothesis_Ruleset
{
 private:
    std::unordered_map<std::string,Hypothesis_Rule*> rules_map;  
 public:
    std::string cell_type; 
    Cell_Definition* pCell_Definition; 

    std::vector< Hypothesis_Rule > rules; 

    Hypothesis_Ruleset(); // done 

    Hypothesis_Rule* add_behavior( std::string behavior , double min_behavior, double max_behavior ); // done 
    Hypothesis_Rule* add_behavior( std::string behavior ); // done 

    // ease of access functions 

    Hypothesis_Rule* find_behavior( std::string name ); // done 
    Hypothesis_Rule& operator[]( std::string name ); // done 
 //   Hypothesis_Rule& access_behavior()
//    void add_signal( std::string behavior, )

    void apply( Cell* pCell ); 

    void sync_to_cell_definition( Cell_Definition* pCD ); // done 
    void sync_to_cell_definition( std::string cell_name ); // done 

    void display( std::ostream& os ); // done 
    void detailed_display( std::ostream& os ); // done 
}; 

// add this to cell behaviors 
double get_single_base_behavior( Cell_Definition* pCD , std::string name ); 

// extern std::map< Cell_Definition* , Hypothesis_Ruleset > hypothesis_rulesets; 


void intialize_hypothesis_rulesets( void ); 

Hypothesis_Ruleset& access_ruleset( Cell_Definition* pCD ); 
Hypothesis_Ruleset* find_ruleset( Cell_Definition* pCD ); 

void add_rule( std::string cell_type, std::string signal, std::string behavior , std::string response ); 

void set_hypothesis_parameters(std::string cell_type, std::string signal, std::string behavior , 
   double half_max, double hill_power ); 
void set_behavior_parameters( std::string cell_type, std::string behavior, 
   double min_value, double max_value ); 
void set_behavior_parameters( std::string cell_type, std::string behavior, 
   double min_value, double base_value , double max_value ); 
void set_behavior_base_value( std::string cell_type, std::string behavior, double base_value ); 


void apply_ruleset( Cell* pCell ); 


void display_hypothesis_rulesets( std::ostream& os ); 
void detailed_display_hypothesis_rulesets( std::ostream& os ); 

void rule_phenotype_function( Cell* pCell, Phenotype& phenotype, double dt ); 

// some helper functions 
std::vector<double> linear_response_to_Hill_parameters( double s0, double s1 ); 
std::vector<double> Hill_response_to_linear_parameters( double half_max , double Hill_power ); 



