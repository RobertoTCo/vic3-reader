"""
Define the utils to manage files for plain-text objects with v3 saves information. 

It automatically defines if we read a json file if save was already converted to json standard
or we read the plain text. 
"""

from pathlib import Path
from typing import Dict, Tuple
import json


class Vic3Reader():
	"""
	Automatise the logic to convert a v3 save to Python dictionary
	or optionally read the cached JSON. 
	
	It also provides a clean method to create cached JSON in a expected 
	relative route.

	- use_json: bool. If True, guess the expected JSON route from the provided path.

	- Method save_as_json() to save a JSON version in the expected route of the project.
	"""
	def __init__(self, 
			  path: Path,
			  use_json: bool = True
			  ):

		self.nominated_json_path = nominate_cached_json(path)
		
		if use_json and self.nominated_json_path.is_file():
			path = self.nominated_json_path

		self.extension, text = read(path)
		self.data = manage_parsing(self.extension, text)

	def save_as_json(self, data: Dict, override: bool = False) -> None:
		"""
		Saves the 'data' dictionary as a '.json' file in the 'json/' subfolder
		of the parent directory of 'path', using the same stem as 'path'.

		Args:
			data: Dict. Vic3 save data after readig file.
			override: bool. If False, do not save new JSON when JSON already exists.
		"""
		json_file = self.nominated_json_path

		# This is to control behaviour when using with multiple calls
		if json_file.is_file() and not override:
			return
		
		with open(json_file, 'w', encoding='utf-8') as f:
				json.dump(data, f, indent=4, ensure_ascii=False)

		
	

def manage_parsing(extension: str, text: str) -> Dict:

	if extension == '.json':
		return json.loads(text)
	
	from vic3_reader.parser import parser
	
	parsed = parser.parse(text)

	return dict(parsed)


def read(path: Path) -> Tuple[str, str]:
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