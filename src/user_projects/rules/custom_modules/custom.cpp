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

#include "./custom.h"

void create_cell_types( void )
{
	// set the random seed 
	SeedRandom( parameters.ints("random_seed") );  
	
	/* 
	   Put any modifications to default cell definition here if you 
	   want to have "inherited" by other cell types. 
	   
	   This is a good place to set default functions. 
	*/ 
	
	initialize_default_cell_definition(); 
	cell_defaults.phenotype.secretion.sync_to_microenvironment( &microenvironment ); 
	
	cell_defaults.functions.volume_update_function = standard_volume_update_function;
	cell_defaults.functions.update_velocity = standard_update_cell_velocity;

	cell_defaults.functions.update_migration_bias = NULL; 
	cell_defaults.functions.update_phenotype = NULL; // update_cell_and_death_parameters_O2_based; 
	cell_defaults.functions.custom_cell_rule = NULL; 
	cell_defaults.functions.contact_function = NULL; 
	
	cell_defaults.functions.add_cell_basement_membrane_interactions = NULL; 
	cell_defaults.functions.calculate_distance_to_membrane = NULL; 
	
	/*
	   This parses the cell definitions in the XML config file. 
	*/
	
	initialize_cell_definitions_from_pugixml(); 

	/*
	   This builds the map of cell definitions and summarizes the setup. 
	*/
		
	build_cell_definitions_maps(); 

	/*
	   This intializes cell signal and response dictionaries 
	*/

	setup_signal_behavior_dictionaries(); 	

	/* 
	   Put any modifications to individual cell definitions here. 
	   
	   This is a good place to set custom functions. 
	*/ 
	
	cell_defaults.functions.update_phenotype = phenotype_function; 
	cell_defaults.functions.custom_cell_rule = custom_function; 
	cell_defaults.functions.contact_function = contact_function; 
	
	/*
	   This builds the map of cell definitions and summarizes the setup. 
	*/
		
	display_cell_definitions( std::cout ); 
	
	return; 
}

void setup_microenvironment( void )
{
	// set domain parameters 
	
	// put any custom code to set non-homogeneous initial conditions or 
	// extra Dirichlet nodes here. 
	
	// initialize BioFVM 
	
	initialize_microenvironment(); 	
	
	return; 
}

void setup_tissue( void )
{
	double Xmin = microenvironment.mesh.bounding_box[0]; 
	double Ymin = microenvironment.mesh.bounding_box[1]; 
	double Zmin = microenvironment.mesh.bounding_box[2]; 

	double Xmax = microenvironment.mesh.bounding_box[3]; 
	double Ymax = microenvironment.mesh.bounding_box[4]; 
	double Zmax = microenvironment.mesh.bounding_box[5]; 
	
	if( default_microenvironment_options.simulate_2D == true )
	{
		Zmin = 0.0; 
		Zmax = 0.0; 
	}
	
	double Xrange = Xmax - Xmin; 
	double Yrange = Ymax - Ymin; 
	double Zrange = Zmax - Zmin; 
	
	// create some of each type of cell 
	
	Cell* pC;
	
	for( int k=0; k < cell_definitions_by_index.size() ; k++ )
	{
		Cell_Definition* pCD = cell_definitions_by_index[k]; 
		std::cout << "Placing cells of type " << pCD->name << " ... " << std::endl; 
		for( int n = 0 ; n < parameters.ints("number_of_cells") ; n++ )
		{
			std::vector<double> position = {0,0,0}; 
			position[0] = Xmin + UniformRandom()*Xrange; 
			position[1] = Ymin + UniformRandom()*Yrange; 
			position[2] = Zmin + UniformRandom()*Zrange; 
			
			pC = create_cell( *pCD ); 
			pC->assign_position( position );
		}
	}
	std::cout << std::endl; 
	
	// load cells from your CSV file (if enabled)
	load_cells_from_pugixml(); 	
	
	return; 
}

std::vector<std::string> my_coloring_function( Cell* pCell )
{ return paint_by_number_cell_coloring(pCell); }

void phenotype_function( Cell* pCell, Phenotype& phenotype, double dt )
{ return; }

void custom_function( Cell* pCell, Phenotype& phenotype , double dt )
{ return; } 

void contact_function( Cell* pMe, Phenotype& phenoMe , Cell* pOther, Phenotype& phenoOther , double dt )
{ return; } 

Hypothesis_Rule::Hypothesis_Rule()
{
	signals_map.empty(); 

	behavior = "none"; 
	base_value = 1.0; 
	max_value = 10.0; 
	min_value = 0.1; 

	signals.empty(); 
	responses.empty(); 
	half_maxes.empty(); 
	hill_powers.empty(); 

	up_signals.empty(); 
	up_half_maxes.empty(); 
	up_hill_powers.empty(); 

	down_signals.empty(); 
	down_half_maxes.empty(); 
	down_hill_powers.empty(); 

	cell_type = "none"; 
	pCell_Definition = NULL; 

	return; 
}

std::string convert_bool_to_response( bool input )
{
	if( input )
	{ return "increases"; }
	return "decreases"; 
}

double extended_Hill_response_function( std::vector<double> signals, std::vector<double> half_maxes , std::vector<double> hill_powers )
{
	double temp1 = 0.0; 
	double temp2 = 0.0; 
	double temp3 = 0.0; 
	// create the generalized (s^h), stored in temp1; 
	for( int j=0 ; j < signals.size(); j++ )
	{
		temp2 = signals[j];     // s
		temp2 /= half_maxes[j]; // s/s_half 
		temp3 = pow( temp2 , hill_powers[j] ); // (s/s_half)^h 
		temp1 += temp3; 
	}
	temp2 = temp1;   // numerator (S^h)
	temp1 += 1.0;    // denominator (1+S^h)
	temp2 /= temp1;  // numerator/denominator = S^h / (1+S^h)
	return temp2; 
}

void Hypothesis_Rule::display( std::ostream& os )
{
	os << "For cell type " << cell_type << ": " << std::endl; 
	for( int j=0; j < signals.size(); j++ )
	{ os << signals[j] << " " << convert_bool_to_response( responses[j] ) << " " << behavior << std::endl; }

	return; 
}

void Hypothesis_Rule::reduced_display( std::ostream& os )
{
	for( int j=0; j < signals.size(); j++ )
	{ os << signals[j] << " " << convert_bool_to_response( responses[j] ) << " " << behavior << std::endl; }

	return; 
}

void Hypothesis_Rule::detailed_display( std::ostream& os )
{
	// os << "For cell type " << cell_type << ": " << std::endl; 
	os << behavior << " is modulated from " << min_value << " to " << max_value << " with a base value of " << base_value << std::endl; 
	os << "--------------------------------------------------------" << std::endl; 
	for( int j=0; j < signals.size(); j++ )
	{
		os << "\t" << signals[j] << " " << convert_bool_to_response( responses[j] ) << " " << behavior
			<< " with half-max " << half_maxes[j] << " and Hill power " << hill_powers[j] << std::endl; 
	}
	return; 
}


void Hypothesis_Rule::add_signal( std::string signal , double half_max , double hill_power , std::string response )
{
	// check to see if it's already there 
	int n = find_signal(signal); 
	// if so, then just warn and exit.  
	if( n > -1 )
	{
		std::cout << "Warning! Signal " << signal << " was already part of the rule. Ignoring input." << 
		std::endl; 

		return; 
	}

	signals_map[signal] = signals_map.size(); 

	bool bResponse = false; // true if up-regulate, false if down
	if( response == "increase" || response == "increases" || response == "promotes" )
	{ bResponse = true; }

	signals.push_back( signal ); 
	half_maxes.push_back( half_max ); 
	hill_powers.push_back( hill_power );
	responses.push_back( bResponse ); 

	// separate into up and down for our convenience 
	if( bResponse == true )
	{
		up_signals.push_back( signal ); 
		up_half_maxes.push_back( half_max ); 
		up_hill_powers.push_back( hill_power ); 
	}
	else
	{
		down_signals.push_back( signal ); 
		down_half_maxes.push_back( half_max ); 
		down_hill_powers.push_back( hill_power ); 
	}
	return; 
}

void Hypothesis_Rule::add_signal( std::string signal , std::string response )
{ return add_signal( signal, 0.1 , 2.0 , response ); }

double Hypothesis_Rule::evaluate( std::vector<double> signal_values )
{
	// create signals 
	std::vector<double> up_signal(0,0); //  up_signals.size() , 0.0 ); 
	std::vector<double> down_signal(0,0); //  down_signals.size() , 0.0 ); 

	for( int j=0; j < signal_values.size(); j++ )
	{ 
		if( responses[j] )
		{ up_signal.push_back( signal_values[j]);  }
		else
		{ down_signal.push_back( signal_values[j]);  }
	}

	// up-regulation part 
	double HU = extended_Hill_response_function(up_signal,up_half_maxes,up_hill_powers); 
	double U = base_value + (max_value-base_value)*HU; 

	// then the down-regulation part 
	double DU = extended_Hill_response_function(down_signal,down_half_maxes,down_hill_powers); 
	double output = U + (min_value-U)*DU; 

	return output; 
}

double Hypothesis_Rule::evaluate( Cell* pCell )
{
	// construct signal vector 
	std::vector<double> signal_values( signals.size() , 0.0 ); 
	for( int i=0; i < signals.size(); i++ )
	{ signal_values[i] = get_single_signal( pCell , signals[i] ); }

	std::cout << signal_values << std::endl; 

	return evaluate( signal_values ); 
}

void Hypothesis_Rule::apply( Cell* pCell )
{
	// evaluate the rule 
	double param = evaluate( pCell ); 

	// apply it ot the appropriate behavior 
	set_single_behavior( pCell , behavior , param ); 

	return; 
}

void Hypothesis_Rule::sync_to_cell_definition( Cell_Definition* pCD )
{
	cell_type = pCD->name; 
	pCell_Definition = pCD; 

	if( pCD == NULL )
	{ return; }

	// sync base behavior 
	base_value = get_single_base_behavior(pCD,behavior); 

	return; 
}

void Hypothesis_Rule::sync_to_cell_definition( std::string cell_name )
{ return sync_to_cell_definition( find_cell_definition(cell_name) ); }

int Hypothesis_Rule::find_signal( std::string name )
{
	auto search = signals_map.find(name);

	if( search == signals_map.end() )
	{ return -1; }

	return search->second; 
}

void Hypothesis_Rule::set_half_max( std::string name , double hm )
{	
	int n = find_signal( name ); 
	if( n < 0 )
	{ return; }

	half_maxes[n] = hm;

	if( responses[n] == true ) 
	{
		for( int m=0; m < up_signals.size(); m++ )
		{
			if( up_signals[m] == name )
			{ up_half_maxes[m] = hm; }
		}	
	}
	else
	{
		for( int m=0; m < down_signals.size(); m++ )
		{
			if( down_signals[m] == name )
			{ down_half_maxes[m] = hm; }
		}
	}
	return; 
}

void Hypothesis_Rule::set_hill_power( std::string name , double hp )
{
	int n = find_signal( name ); 
	if( n < 0 )
	{ return; }

	hill_powers[n] = hp;
	if( responses[n] == true ) 
	{   
		for( int m=0; m < up_signals.size(); m++ )
		{
			if( up_signals[m] == name )
			{ up_hill_powers[m] = hp; }
		}		
	}
	else
	{
		for( int m=0; m < up_signals.size(); m++ )
		{
			if( down_signals[m] == name )
			{ down_hill_powers[m] = hp; }
		}	
	}
	return; 
}

void Hypothesis_Rule::set_response( std::string name , std::string response )
{
	int n = find_signal( name ); 
	if( n < 0 )
	{ return; }

	bool bResponse = false; // true if up-regulate, false if down
	if( response == "increase" || response == "increases" || response == "promotes" )
	{ bResponse = true; }

	// this is already my response? if so exit 
	if( bResponse == responses[n] )
	{ return; }


	if( responses[n] == true ) 
	{   
		// need to switch from up to down 
			// find current index 
		int ci = -1; 
		for( int m=0; m < up_signals.size(); m++ )
		{
			if( up_signals[m] == name )
			{ ci = m; }
		}
			// swap last inot that position 
		up_half_maxes[ci] = up_half_maxes.back(); 
		up_hill_powers[ci] = up_hill_powers.back(); 
		up_signals[ci] = up_signals.back(); 

			// reduce size by one

		up_half_maxes.pop_back(); 
		up_hill_powers.pop_back(); 
		up_signals.pop_back(); 

			// move to the other side 

		down_half_maxes.push_back( half_maxes[n] ); 
		down_hill_powers.push_back( hill_powers[n]); 
		down_signals.push_back( signals[n] ); 
	}
	else
	{
		// need to switch from down to up 
			// find current index 
		int ci = -1; 
		for( int m=0; m < down_signals.size(); m++ )
		{
			if( down_signals[m] == name )
			{ ci = m; }
		}
			// swap last inot that position 
		down_half_maxes[ci] = down_half_maxes.back(); 
		down_hill_powers[ci] = down_hill_powers.back(); 
		down_signals[ci] = down_signals.back(); 

			// reduce size by one

		down_half_maxes.pop_back(); 
		down_hill_powers.pop_back(); 
		down_signals.pop_back(); 

			// move to the other side 

		up_half_maxes.push_back( half_maxes[n] ); 
		up_hill_powers.push_back( hill_powers[n]); 
		up_signals.push_back( signals[n] ); 
	}

	responses[n] = bResponse; 

	return; 
}

/* add this to the core library! */ 

double get_single_base_behavior( Cell_Definition* pCD , std::string name )
{
	static int m = microenvironment.number_of_densities(); 
	static int n = cell_definition_indices_by_name.size(); 

	int index = find_behavior_index(name); 

	if( index < 0 )
	{
		std::cout << "Warning: attempted to get behavior with unknown index " << index << std::endl	
				  << "         I'm ignoring it, but you should fix it!" << std::endl; 
		return 0.0; 
	}

	// substrate-related behaviors 

	// first m entries are secretion 
	static int first_secretion_index = find_behavior_index( microenvironment.density_names[0] + " secretion" ); // 0; 
	if( index >= first_secretion_index && index < first_secretion_index + m )
	{ return pCD->phenotype.secretion.secretion_rates[index-first_secretion_index]; }

	// next m entries are secretion targets
	static int first_secretion_target_index = find_behavior_index( microenvironment.density_names[0] + " secretion target" ); // m; 
	if( index >= first_secretion_target_index && index < first_secretion_target_index + m )
	{ return pCD->phenotype.secretion.saturation_densities[index-first_secretion_target_index]; }

	// next m entries are uptake rates
	static int first_uptake_index = find_behavior_index( microenvironment.density_names[0] + " uptake" );  // 2*m; 
	if( index >= first_uptake_index && index < first_uptake_index + m )
	{ return pCD->phenotype.secretion.uptake_rates[index-first_uptake_index]; }

	// next m entries are net export rates 
	static int first_export_index = find_behavior_index( microenvironment.density_names[0] + " export" ); //  3*m; 
	if( index >= first_export_index && index < first_export_index + m )
	{ return pCD->phenotype.secretion.net_export_rates[index-first_export_index]; }

	// cycle entry (exit from phase 0) and exit from up to 5 more phases 
	static int first_cycle_index = find_behavior_index("exit from cycle phase 0" ); //  4*m; 
	int max_cycle_index = pCD->phenotype.cycle.model().phases.size(); 
	if( max_cycle_index > 6 )
	{
		max_cycle_index = 6; 
		std::cout << "Warning: Standardized behaviors only support exit rate from the first 6 phases of a cell cycle!" << std::endl 
		          << "         Ignoring any later phase exit rates." << std::endl; 
	}
	if( index >= first_cycle_index && index < first_cycle_index + 6 )
	{
		int ind = index - first_cycle_index; 
		if( ind < max_cycle_index )
		{ return pCD->phenotype.cycle.data.exit_rate( ind ); }
		return 0.0; 
	}

	static int apoptosis_index = pCD->phenotype.death.find_death_model_index( PhysiCell_constants::apoptosis_death_model ); 
	static int necrosis_index = pCD->phenotype.death.find_death_model_index( PhysiCell_constants::necrosis_death_model ); 

	static int apop_param_index = find_behavior_index( "apoptosis"); 
	static int necr_param_index = find_behavior_index( "necrosis"); 

	// apoptosis 
	if( index == apop_param_index )
	{ return pCD->phenotype.death.rates[apoptosis_index]; }

	// necrosis 
	if( index == necr_param_index )
	{ return pCD->phenotype.death.rates[necrosis_index]; }

	// migration speed
	static int migr_spd_index = find_behavior_index( "migration speed"); 
	if( index == migr_spd_index )
	{ return pCD->phenotype.motility.migration_speed; }

	// migration bias 
	static int migr_bias_index = find_behavior_index( "migration bias"); 
	if( index == migr_bias_index )
	{ return pCD->phenotype.motility.migration_bias; }

	// migration persistence time
	static int migr_pt_index = find_behavior_index( "migration persistence time"); 
	if( index == migr_pt_index )
	{ return pCD->phenotype.motility.persistence_time; }

	// chemotactic sensitivities 
	static int first_chemotaxis_index = find_behavior_index( "chemotactic response to " + microenvironment.density_names[0] ); 
	if( index >= first_chemotaxis_index && index < first_chemotaxis_index + m )
	{ return pCD->phenotype.motility.chemotactic_sensitivities[index-first_chemotaxis_index]; }

	// cell-cell adhesion 
	static int cca_index = find_behavior_index( "cell-cell adhesion" ); 
	if( index == cca_index )
	{ return pCD->phenotype.mechanics.cell_cell_adhesion_strength; }

	// cell-cell "springs"
	static int cca_spring_index = find_behavior_index( "cell-cell adhesion elastic constant" );  
	if( index == cca_spring_index )
	{ return pCD->phenotype.mechanics.attachment_elastic_constant; }

    // cell adhesion affinities 
	static int first_affinity_index = find_behavior_index("adhesive affinity to " + cell_definitions_by_type[0]->name ); 
	if( index >= first_affinity_index && index < first_affinity_index + n )
	{ return pCD->phenotype.mechanics.cell_adhesion_affinities[index-first_affinity_index]; }

	// max relative maximum adhesion distance 
	static int max_adh_index = find_behavior_index("relative maximum adhesion distance" ); 
	if( index == max_adh_index )
	{ return pCD->phenotype.mechanics.relative_maximum_adhesion_distance; }

	// cell-cell repulsion 
	static int ccr_index = find_behavior_index("cell-cell repulsion" ); 
	if( index == ccr_index )
	{ return pCD->phenotype.mechanics.cell_cell_repulsion_strength; }

	// cell-BM adhesion 
	static int cba_index = find_behavior_index("cell-BM adhesion" ); 
	if( index == cba_index )
	{ return pCD->phenotype.mechanics.cell_BM_adhesion_strength; }
	
	// cell-BM repulsion 
	static int cbr_index = find_behavior_index("cell-BM repulsion" ); 
	if( index == cbr_index )
	{ return pCD->phenotype.mechanics.cell_BM_repulsion_strength; }

	// dead cell phagocytosis
	static int dead_phag_index = find_behavior_index("phagocytose dead dell" ); 
	if( index == dead_phag_index )
	{ return pCD->phenotype.cell_interactions.dead_phagocytosis_rate; }

    // phagocytosis of each live cell type 
	static int first_phagocytosis_index = find_behavior_index( "phagocytose " + cell_definitions_by_type[0]->name ); 
	if( index >= first_phagocytosis_index && index < first_phagocytosis_index + n )
	{ return pCD->phenotype.cell_interactions.live_phagocytosis_rates[index-first_phagocytosis_index]; } 

	// attack of each live cell type 
	static int first_attack_index = find_behavior_index( "attack " + cell_definitions_by_type[0]->name ); 
	if( index >= first_attack_index && index < first_attack_index + n )
	{ return pCD->phenotype.cell_interactions.attack_rates[index-first_attack_index]; } 

	// fusion 
	static int first_fusion_index = find_behavior_index( "fuse to " + cell_definitions_by_type[0]->name ); 
	if( index >= first_fusion_index && index < first_fusion_index + n )
	{ return pCD->phenotype.cell_interactions.fusion_rates[index-first_fusion_index]; } 

 	// transformation 
	static int first_transformation_index = find_behavior_index( "transform to " + cell_definitions_by_type[0]->name ); 
	if( index >= first_transformation_index && index < first_transformation_index + n )
	{ return pCD->phenotype.cell_transformations.transformation_rates[index-first_transformation_index]; } 

	// custom behavior
	static int first_custom_ind = find_behavior_index( "custom 0"); 
	static int max_custom_ind = first_custom_ind + pCD->custom_data.variables.size();  
	if( first_custom_ind >= 0 && index >= first_custom_ind && index < max_custom_ind )
	{ return pCD->custom_data.variables[index-first_custom_ind].value; }

	return -1; 
}

Hypothesis_Ruleset::Hypothesis_Ruleset()
{
	cell_type = "none"; 
	pCell_Definition = NULL; 

	rules.empty(); 
	rules_map.empty(); 

	return; 
}

void Hypothesis_Ruleset::display( std::ostream& os )
{
	os << "Behavioral rules for cell type " << cell_type << ":" << std::endl; 
	os << "===================================================" << std::endl; 
	for( int i=0; i < rules.size() ; i++ )
	{ rules[i].reduced_display(os); }
	os << std::endl; 
	return; 
}

void Hypothesis_Ruleset::detailed_display( std::ostream& os )
{
	os << "Behavioral rules for cell type " << cell_type << ":" << std::endl; 
	os << "===================================================" << std::endl; 
	for( int i=0; i < rules.size() ; i++ )
	{ rules[i].detailed_display(os); }
	os << std::endl; 
	return; 
}


void Hypothesis_Ruleset::sync_to_cell_definition( Cell_Definition* pCD )
{
	pCell_Definition = pCD; 
	cell_type = pCD->name; 

	for( int i=0; i < rules.size(); i++ )
	{ rules[i].sync_to_cell_definition(pCD); }

	return; 
}

Hypothesis_Rule* Hypothesis_Ruleset::add_behavior( std::string behavior , double min_behavior, double max_behavior )
{
	// first, check. Is there already a ruleset? 
	auto search = rules_map.find( behavior ); 
		// if not, add it 
	if( search == rules_map.end() )
	{
		Hypothesis_Rule hr; 

		hr.behavior = behavior; 
		hr.sync_to_cell_definition( pCell_Definition ); 
		hr.min_value = min_behavior; 
		hr.max_value = max_behavior; 

		rules.push_back( hr ); 
		Hypothesis_Rule* pHR = &(rules.back()); 
		rules_map[ behavior ] = pHR; 

		return pHR; 
	}
		// otherwise, edit it 
	Hypothesis_Rule* pHR = search->second; 
	pHR->min_value = min_behavior; 
	pHR->max_value = max_behavior; 

	return pHR; 
}

Hypothesis_Rule* Hypothesis_Ruleset::add_behavior( std::string behavior )
{ 
	double min_behavior = 0.1; 
	double max_behavior = 1.0; 
	return Hypothesis_Ruleset::add_behavior( behavior, min_behavior, max_behavior );
}

void Hypothesis_Ruleset::sync_to_cell_definition( std::string cell_name )
{ return sync_to_cell_definition( find_cell_definition(cell_name) ); }

Hypothesis_Rule* Hypothesis_Ruleset::find_behavior( std::string name )
{
    auto search = rules_map.find( name); 
	if( search == rules_map.end() )
	{
		std::cout << "Warning! Ruleset does not contain " << name << std::endl; 
		std::cout << "         Returning NULL." << std::endl; 
		return NULL; 
	}

	return search->second; 
}

Hypothesis_Rule& Hypothesis_Ruleset::operator[]( std::string name )
{
	Hypothesis_Rule* pHR = find_behavior(name);
	return *pHR; 
} 

void Hypothesis_Ruleset::apply( Cell* pCell )
{
	for( int n=0; n < rules.size() ; n++ )
	{ rules[n].apply( pCell ); }
	return; 
}

std::map< Cell_Definition* , Hypothesis_Ruleset > hypothesis_rulesets; 

void add_hypothesis_ruleset( Cell_Definition* pCD )
{
	auto search = hypothesis_rulesets.find( pCD );
	if( search == hypothesis_rulesets.end() )
	{
		Hypothesis_Ruleset HRS; 
		HRS.sync_to_cell_definition( pCD ); 
		hypothesis_rulesets[pCD] = HRS; 
	}
	return; 
}


void intialize_hypothesis_rulesets( void )
{
	hypothesis_rulesets.empty(); 

	for( int n; n < cell_definitions_by_index.size() ; n++ )
	{
		Cell_Definition* pCD = cell_definitions_by_index[n]; 
		add_hypothesis_ruleset(pCD); 
	}

	return; 
}

Hypothesis_Ruleset& access_ruleset( Cell_Definition* pCD )
{ return hypothesis_rulesets[pCD]; }

Hypothesis_Ruleset* find_ruleset( Cell_Definition* pCD )
{ return &(hypothesis_rulesets[pCD]); }

void display_hypothesis_rulesets( std::ostream& os )
{
	for( int n=0 ; n < cell_definitions_by_index.size() ; n++ )
	{ hypothesis_rulesets[ cell_definitions_by_index[n] ].display( os ); }

	return; 
}

void detailed_display_hypothesis_rulesets( std::ostream& os )
{
	for( int n=0 ; n < cell_definitions_by_index.size() ; n++ )
	{ hypothesis_rulesets[ cell_definitions_by_index[n] ].detailed_display( os ); }

	return; 
}



void add_rule( std::string cell_type, std::string signal, std::string behavior , std::string response )
{
	Cell_Definition* pCD = find_cell_definition(cell_type); 
	Hypothesis_Ruleset* pHRS = find_ruleset( pCD ); 

	pHRS->add_behavior(behavior); 
	(*pHRS)[behavior].add_signal(signal,response); 

	return; 
}

void set_hypothesis_parameters(std::string cell_type, std::string signal, std::string behavior , 
   double half_max, double hill_power )
{
	Cell_Definition* pCD = find_cell_definition( cell_type ); 
	if( find_ruleset(pCD) == NULL )
	{ std::cout << "Error. No hypothesis ruleset for " << cell_type << ". Ignoring."<< std::endl; return; }

	if( hypothesis_rulesets[pCD].find_behavior(behavior) == NULL )
	{ std::cout << "Error. No " << behavior << " rules for " << cell_type << ". Ignoring."<< std::endl; return; }
		
	if( hypothesis_rulesets[pCD][behavior].find_signal(signal) < 0 )
	{ std::cout << "Error. " << behavior << "rules for " << cell_type << " do not involve " << signal << ". Ignoring."<< std::endl; return; }
	
	hypothesis_rulesets[pCD][behavior].set_half_max(signal,half_max); 
	hypothesis_rulesets[pCD][behavior].set_hill_power(signal,hill_power); 
	
	return; 
}

void set_behavior_parameters( std::string cell_type, std::string behavior, 
   double min_value, double max_value )
{
	Cell_Definition* pCD = find_cell_definition( cell_type ); 
	if( find_ruleset(pCD) == NULL )
	{ std::cout << "Error. No hypothesis ruleset for " << cell_type << ". Ignoring."<< std::endl; return; }

	if( hypothesis_rulesets[pCD].find_behavior(behavior) == NULL )
	{ std::cout << "Error. No " << behavior << " rules for " << cell_type << ". Ignoring."<< std::endl; return; }
	
	hypothesis_rulesets[pCD][behavior].min_value = min_value; 
	hypothesis_rulesets[pCD][behavior].max_value = max_value; 
	
	return;
}

void set_behavior_parameters( std::string cell_type, std::string behavior, 
   double min_value, double base_value , double max_value )
{
	Cell_Definition* pCD = find_cell_definition( cell_type ); 
	if( find_ruleset(pCD) == NULL )
	{ std::cout << "Error. No hypothesis ruleset for " << cell_type << ". Ignoring."<< std::endl; return; }

	if( hypothesis_rulesets[pCD].find_behavior(behavior) == NULL )
	{ std::cout << "Error. No " << behavior << " rules for " << cell_type << ". Ignoring."<< std::endl; return; }
	
	hypothesis_rulesets[pCD][behavior].min_value = min_value; 
	hypothesis_rulesets[pCD][behavior].max_value = max_value; 
	hypothesis_rulesets[pCD][behavior].base_value = base_value; 
	
	return;
}


void set_behavior_base_value( std::string cell_type, std::string behavior, double base_value )
{
	Cell_Definition* pCD = find_cell_definition( cell_type ); 
	if( find_ruleset(pCD) == NULL )
	{ std::cout << "Error. No hypothesis ruleset for " << cell_type << ". Ignoring."<< std::endl; return; }

	if( hypothesis_rulesets[pCD].find_behavior(behavior) == NULL )
	{ std::cout << "Error. No " << behavior << " rules for " << cell_type << ". Ignoring."<< std::endl; return; }
	
	hypothesis_rulesets[pCD][behavior].base_value = base_value; 
	
	return;
}




void apply_ruleset( Cell* pCell )
{
	Cell_Definition* pCD = find_cell_definition( pCell->type_name ); 
	hypothesis_rulesets[pCD].apply( pCell );
	return; 
}

void rule_phenotype_function( Cell* pCell, Phenotype& phenotype, double dt )
{ apply_ruleset( pCell ); }

void my_setup( void ); 

/* add these to core */ 

std::vector<double> linear_response_to_Hill_parameters( double s0, double s1 )
{
	static double tol = 0.1; 
	static double param1 = (1-tol)/tol; 
	static double param2 = log(param1); 

	// half max, then hill power 
	double hm = 0.5* (s0+s1); 

	// hp so that H(s1) ~ (1-tol)
	double hp = round( param2 / log(s1/hm) ); 

	std::vector<double> output = { hm , hp }; 

	return output; 
}

std::vector<double> Hill_response_to_linear_parameters( double half_max , double Hill_power )
{
	static double tol = 0.1; 
	static double param1 = (1-tol)/tol; 
	double param2 = pow( param1 , 1.0/ Hill_power ); 

	// s1 such that H(s1) ~ (1-tol)
	double s1 = half_max * param2; 

	// s0 for symmetry
	double s0 = 2*half_max -s1; 
	if( s0 < 0 )
	{ s0 = 0.0; }

	std::vector<double> output = {s0,s1}; 

	std::cout << output; 


	return output; 
}
