from pathlib import Path
from typing import Dict

PATH = Path('saves/1844 TXT.v3')

def manage_parsing(extension: str, text: str) -> Dict:

	if extension == '.json':
		import json
		return json.loads(text)
	
	from parser import parser
	
	parsed = parser.parse(text)

	return dict(parsed)


if __name__ == '__main__':

	from utils import create_gui, read_file, save_as_json
	from orchestrator import Orchestrator
	from metrics import TAGS

	extension, text = read_file(PATH)

	data = manage_parsing(extension, text)

	if extension != '.json':
		save_as_json(PATH, data)	# cache version 

	
	test = Orchestrator(
		data = data,
		wanted_tags=TAGS
	)

	df = test.to_dataframe()

	print(df)
	
	create_gui(data)