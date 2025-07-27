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

# text = r"""17={
# 	is_main_tag=yes
# 	definition="JAP"
# 	government="gov_shogunate"
# 	dynamic_name={
# 		dynamic_country_name="dyn_c_japan_shogunate"
# 		dynamic_country_adjective="dyn_c_japan_shogunate_adj"
# 	}
# 	map_color=rgb { 45 91 79 }
# 	ruler=3355
# 	heir=16785195
# 	}"""
# extension = '.v3'

if __name__ == '__main__':

	from utils import create_gui, read_file, save_as_json

	extension, text = read_file(PATH)

	data = manage_parsing(extension, text)

	if extension != '.json':
		save_as_json(PATH, data)	# cache version 
	
	create_gui(data)