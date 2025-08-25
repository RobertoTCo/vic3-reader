


if __name__ == '__main__':
	
	from pathlib import Path
	from utils import create_gui
	from metrics import TAGS

	from metrics import get_adm, get_economy

	METRICS = [
		get_economy,
		get_adm,
	]
	
	from orchestrator import Orchestrator
	FOLDER = Path('saves')

	orchestrator = Orchestrator(
			folder_path=FOLDER, 
			wanted_tags=TAGS,
			metrics_fn=METRICS,
			save_as_json=True
			)

	# orchestrator.save_long("result.csv", folder="results")
	orchestrator.save_multiple_sheets("result.xlsx", folder="results")
		
	print(orchestrator)

	# create_gui(data)
