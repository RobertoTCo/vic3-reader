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