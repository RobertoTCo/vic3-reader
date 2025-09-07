# How can I add more metrics?

If you are interested in contributing to this project and add more stats that can be used, feel free to work in the 'metrics' section. You can do any changes that you feel neccesary to implement new functions to extract stats and do a pull request to the main branch for approval. Any support is really appreciated.

Please, always follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) when commiting.

You can also use the [explore_save_with_gui.py](../explore_save_with_gui.py) script to get a interface that lets you to navigate every branch of the save file.


### How is this structured?

(a) The metrics definitions are structured in a set of python modules. Each module implement a set of semantically similar metrics, some examples could be economy, army, diplomacy, etc. 

(b) Also, you can find the [models subfolder](../src/vic3_reader/metrics/models/) that defines the data structure for every section of information using Pydantic. This is used to ensure that required data for every metric is present (validation) and the file logic is in a human-readable format. You may need to edit this part or not, depending on what part of the vic3 saves you need.


### Why are you using pydantic models, reading the whole file and I need to care about all this strict logic?

This is done to support single responsability across the different parts of the vic3-reader and facilitate collaboration without touching other parts of the repository. The metrics subfolder works to make the life easier to the whole repository and needs to align with its dependency. The good side is you only need to focus on this part and forget the rest of the subfolders and main modules!


### So, how can I add my own metrics?

I strongly recommend first to have a look at some examples, like the [economy.py module](../src/vic3_reader/metrics/economy.py) and understand how it uses the [models subfolder](../src/vic3_reader/metrics/models/) to hint what parts of the save is using.

In each module, a main function is defined at the bottom that accept the save data and some parameters and decides what it needs to simplify the work of all the metrics in the module. The save data is a Vic3Save object defined in [the models __init__](../src/vic3_reader/metrics/models/__init__.py), as this is always what the [orchestrator.py](../src/vic3_reader/orchestrator.py) uses to get metrics. The orchestrator is very spoilt and does not care about how metrics are extracted.

For example, the [economy.py module](../src/vic3_reader/metrics/economy.py) implements get_economy() at the bottom, and this is the main function that decides how to work with every function that gets an unique metric. This function can be implemented in the [orchestrator.py](../src/vic3_reader/orchestrator.py) to get all the economy stats that you want.

If you are working with a part of the vic3 save file that does not accomodate the Pydantic models in [models subfolder](../src/vic3_reader/metrics/models/), feel free to create a module in the models folder that define the internal struccture of that part of the file. This always need to be added to the Vic3Save object defined in [the models __init__](../src/vic3_reader/metrics/models/__init__.py). You can import from [the models basic.py](../src/vic3_reader/metrics/models/basic.py) the general objects that are re-used across the whole vic3 file.


### How all this changes can be implemented in the master?

This is going to be kept simple as possible. To push your changes to the master branch, you will need to do a PR for review. If it does not break the code, or it only requires minor editions, it will be likely accepted.

<u> Please, always follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) when commiting. </u>