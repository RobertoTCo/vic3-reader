# Vic3-reader: A custom tool to extract stats & metrics from Victoria 3 games.


### What is this?

With vic3-reader you can automatically extract a set of basic statistics and metrics from your game. This is implemented in a way where you just need to specify a minimum info about where to find the save files and how you want to extract them. This tool implements all the hard work for you and gives you all the info in one file.

Currently, the tool has implemented a set of basic stats related to treasury, debt, population, infamy, standard of living and construction. In the future, other metrics that are not explicitly written in the files may be added to this tool.

<u>If you would like to contribute adding more metrics, please read [How to add more](./documentation//how_to_add_more.md).</u>


### How can I use it?

To use this tool, 

(1) first clone this repository or download the files.

(2) Install dependencies specified in pyproject.toml and uv.lock with UV or another package tool.

(3) Prepare your vic3 save files as plain text. By default, vic3 saves are binarized.

Try [reddit: How to edit/decrypt victoria 3 save files?](https://www.reddit.com/r/victoria3/comments/yg4s7e/how_to_editdecrypt_victoria_3_save_files/) or you can use the debug console in-game to save files as plain text, [Youtube: How to Use the In-Game Editor](https://www.youtube.com/watch?v=V49oRZUkDDI&embeds_referring_euri=https%3A%2F%2Fwww.bing.com%2F&embeds_referring_origin=https%3A%2F%2Fwww.bing.com&source_ve_path=Mjg2NjY).

(4) Edit the [config.py](./config.py) to specify the location of your plain-text saves, how to save the stats, what metrics you want and which countries. Save changes.

(5) Execute [main.py](./main.py) after editing the config.py file. The execution may take a while depending on how many saves you use and your hardware.*

*When reading a plain-text Victoria3 save, it usually takes between 2 to 5 minutes to parse a save. If you execute the programme multiple times for the same saves, you may want to consider use the option `CACHE_AS_JSON=TRUE` in [config.py](./config.py). This will save a JSON representation of your save. But be careful, this JSON files have a big size, around 500MB.
 
<br>
 
# I want to understand the code

### How does this tool work?

This tool is composed of 4 main setions. 

(a) Specify in [config.py](./config.py) the variables to execute the programme. Then, execute the [main.py](./main.py) file to extract the metrics.

(b) The [Metrics modules](./src/vic3_reader/metrics/) define how different stats are extracted from the save. To accurately navigate through vic3 data, the [models subfolder](./src/vic3_reader/metrics/models/) defines the data structure for every section where metrics are extracted.

(c) The [parser modules](./src/vic3_reader/parser/) define how to read the sintax of a vic3 save file by a DSL and how to translate it to a Python dictionary when reading a file.

(d) The [orchestrator.py](./src/vic3_reader/orchestrator.py) module is in charge of combining all the logic, iterating through multiple files, reading and extrating metrics and providing methods to save them as different data formats.


# License

MIT License