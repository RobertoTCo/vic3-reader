
def main():
	from config import CACHE_AS_JSON, FILE_RESULTS, FOLDER_RESULTS, FOLDER_SAVES, METRICS, TAGS


	from vic3_reader.orchestrator import Orchestrator

	orchestrator = Orchestrator(
			folder_path=FOLDER_SAVES, 
			wanted_tags=TAGS,
			metrics_fn=METRICS,
			save_as_json=CACHE_AS_JSON
			)

	# You can save the table as long format (each row is a year and tag; each column is a metric. )
	# Or you can obtain an excel or ods with a table per metric, in this case each row is a year and each column a tag.

	# For that, use orchestrator.save_long() or orchestrator.save_multiple_sheets(). 

	orchestrator.save_long(FILE_RESULTS, folder=FOLDER_RESULTS)
	# orchestrator.save_multiple_sheets(FILE_RESULTS, folder=FOLDER_RESULTS)


if __name__ == '__main__':
	import time
	start = time.time()
	main()
	stop = time.time()
	print("--- %s seconds ---" % (stop - start))