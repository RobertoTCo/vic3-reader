"""
Define the utils to manage files for plain-text objects with v3 saves information. 

It automatically defines if we read a json file if save was already converted to json standard
or we read the plain text. 
"""

from pathlib import Path
from typing import Dict, Tuple, TypeAlias
import json

""" file extension """
Extension: TypeAlias = str 

def read_file(path: Path) -> Tuple[Extension, str]:
	"""
	path of a v3 plain-text file (.v3, .txt, ...).
	It automatically checks if a cached json version is already created and loads it,
	otherwise reads the plain text following v3 structure.

	Returns: tuple with end extension and text
	"""
	json_file = nominate_cached_json(path)

	if json_file.is_file():
		path = json_file

	with open(path, 'r', encoding='utf-8') as file:
		return (path.suffix, file.read() )
	

def nominate_cached_json(path: Path) -> Path:
	parent_dir = path.parent
	json_dir = parent_dir / 'json_saves'
	json_dir.mkdir(parents=True, exist_ok=True)  # Ensure the json folder exists
	return json_dir / (path.name  + '.json')  # e.g., Path('saves/json/prussia_1844.v3.json')
     

def save_as_json(path: Path, data: Dict) -> None:
	"""
	Saves the `data` dictionary as a `.json` file in the `json/` subfolder
	of the parent directory of `path`, using the same stem as `path`.
	"""
	json_dir = path.parent / 'json_saves'
	json_file = json_dir / (path.name  + '.json')

	with open(json_file, 'w', encoding='utf-8') as f:
		json.dump(data, f, indent=4, ensure_ascii=False)


sample: str = """
    meta_data={
	save_game_version=1720704456
	version="1.7.5"
	game_date=1873.1.2.6
	real_date=124.7.27
	name="Ottoman Empire"
	rank=great_power
	flag={
		pattern="pattern_solid.tga"
		color1=red
		colored_emblem={
			color1=white
			color2=white
			texture="ce_crescent.dds"
			instance={
				position={ 0.320000 0.500000 }
				scale={ 0.660000 0.660000 }
			}
		}
		colored_emblem={
			color1=white
			color2=white
			texture="ce_star_08.dds"
			instance={
				position={ 0.580000 0.500000 }
				scale={ 0.360000 0.360000 }
			}
		}
	}
	dlcs={ "Voice of the People Preorder" "Region Pack 1" "Sphere of Influence" "Voice of the People" "American Buildings Pack" }
	game_rules={
		settings={ achievements_allowed standard_ai_behavior standard_ai_aggression plausible_formable_nations plausible_releasable_nations moderate_consolidation allow_monument_effects allow_subject_flags allow_subject_map_color }
	}
	achievement_eligibility=no
	ironman=no
	number_of_players=7
}
ironman={
	ironman=no
	date=1.1.1
	save_game=""
	save_interval=three_months
	storage=local
}
playthrough_id="9894ada2-e271-4f37-9327-b35a879d159d"
date=1873.1.2.6
seed=3629941324
seed_count=53103107
speed=2
first_start=no
previous_played={ {
		idtype=1
		name="MartinLooterKings"
	} {
		idtype=3
		name="JoniHD4"
	} {
		idtype=4
		name="GonsuPeppaH"
	} {
		idtype=5
		name="Patitodo"
	} {
		idtype=29
		name="GeneralMax"
	} {
		idtype=62
		name="Hospitalet Resident"
	} {
		idtype=94
		name="AvengerDay"
	} {
		idtype=4294967295
		name="Arthur Van Matterhorn"
	} }
counters={
command=2157494
tick=54026
week=1930
province_owner=53137
province_theater=252031
province_occupation=1215
state_provinces=50969
wars=349
diplomatic_play_participants=2936
markets=411
create_destroy_markets=4641
fully_executed_commands=2157494
fully_executed_non_ai_commands=578223
modifiers=645827
canal_connections=5
constructions_progressed=1930
num_countries=1148
travel_connection=77507
num_power_blocs=13
}
variables={
	data={  {
			flag="krakatoa_var"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="krakatoa_crop_failure_var"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="peoples_springtime_happened"
			tick=0
			data={
				type=boolean
				identity=1
			}
		} {
			flag="humanita_fortress_global_var"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="fra_annexed_savoy"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="fra_savoy_sardinia"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="labour_movement_researched"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="suez_canal_purchase_var"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="oregon_trail_mapped"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="improve_living_conditions_global_var"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="dabrowski_spawn"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="rus_bought_outer_manchuria"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="rus_chuguchak_protocol"
			data={
				type=boolean
				identity=1
			}
		} {
			flag="caucasus_consolidated_var"
			data={
				type=boolean
				identity=1
			}
		} }
}
provinces={
	0={
	}
	1={
		state=4
		building="building_wheat_farm"
	}
	2={
		state=4
		building="building_sulfur_mine"
	}
	3={
		state=4
		building="building_livestock_ranch"
	}
	4={
		state=4
		building="building_sulfur_mine"
	}
	5={
		state=4
		building="building_urban_center"
	}
}
3120564021={
	type="laborers"
	workforce=139
	dependents=513
	location=314
	interest_group_support={ 0 2.2365 0 0.00072 0.00198 0 3.33284 0.13334 }
	culture=70
	workplace=7782
	religion="sunni"
	num_literate=4
	qualifications={ 15 0=1.39916 2=3.46851 4=11.65055 5=35.71616 6=7.99501 7=46.5898 9=23.49619 12=12.24581 }
	wealth=3
	previous_quality_of_life=3
	loyalists_and_radicals=-275
	weekly_budget={ 2.81093 0 6.4089 0 0 0 0 -8.42256 0 -0.23892 0 0 -0.07021 }
	job_satisfaction=-89.80069
	partial_growth_wa=0.44705
	partial_growth_dn=-0.01028
	is_accepted_culturally=no
	is_discriminated=yes
}
2046822198={
	type="capitalists"
	workforce=50
	dependents=159
	location=825
	largest_interest_group=10
	interest_group_support={ 2.1965 1.5295 45.2975 0.9755 0 0 0 0 }
	culture=61
	workplace=10440
	religion="orthodox"
	num_literate=36
	qualifications={ 15 0=29.91299 1=4.47363 2=45.8372 3=50 4=18.32684 5=38.04319 6=14.94478 7=32.82945 9=30.30083 10=0.61161 12=35.17512 }
	wealth=52
	previous_quality_of_life=52
	loyalists_and_radicals=209
	weekly_budget={ 0 0 0 0 325.02343 6.14606 0 -278.55401 0 0 -0.673 0 -26.38887 }
	job_satisfaction=443.62186
	partial_growth_wa=0.70766
	partial_growth_dn=0.62642
}
1090520887={
	type="laborers"
	location=851
	interest_group_support={ 0 0 0 0 0 0 0 0 }
	culture=56
	religion="protestant"
	qualifications={ 15 }
	wealth=14
	previous_quality_of_life=14
	weekly_budget={ 0 0 0 0 0 0 0 0 0 0 0 0 0 }
	job_satisfaction=0
}
"""