from typing import Callable, Dict, List, Sequence, Set, Tuple
from datetime import date
from pathlib import Path

import pandas as pd

from metrics.models import Country, CountryManager, TagIDStr, ValidationError, Vic3Save

from metrics import get_game_date, get_tag_data

from parser.reader import Vic3Reader

none_wanted_tag_error = ( 
    "You must specify which tag IDs are you searching in the save." \
    " These ids are the digit IDs in the save, not the 3 letter tags."
    )
empty_seq_metrics_fn_error = (
    "Empty list of metrics" \
    " You need to provide a list of metrics to extract."
    )

class Orchestrator():
    """
    Object specialised in extrating the defined metrics from multiple files and structuring them in a long table.
    It provides methods to save the result as different file types in long or wide format.
    Note: this class does not distinguish the file format and will attempt to read all files for the specified route.

    Parameters:
    -   folder_path: Path or str. Path to the folder where v3 files are saved. 

    -   wanted_tags: Tag IDs of countries whose metrics will be extracted.

        This ensures efficient computation, overlooking unwanted countries.

    -   metrics_fn: Iterable sequence i.e. List, of functions designed to accept a Vic3save data model and return 
                    a dictionary with a set of metrics. This controls the metrics that will be extracted from the file.

    -   save_as_json: bool, default False. Set as True to save the parsed save data as a JSON in disk to make the reading faster next time.
                    WARNING! The resulting game JSON can be very heavy, around 500MB.

    Attributes:
    -   self.metrics_df: long-format table with metrics (columns) per year and Tag (row multi-index).

        Print in console the created instance to preview the resulting table.

    Methods:
    -   self.save_long(). Use this method to save the self.metrics_df in a specific format supported by Pandas library.
                        The resulting table is a row per year and tag and columns per every metric.

    -   self.save_multiple_sheets(). Use this method to save self.metrics_df as a excel or .ods format 
                        where each page isfor a metric, a row per year and each column is a tag.
    """

    def __init__(
            self, 
            folder_path: Path | str,
            wanted_tags: Set[TagIDStr],
            metrics_fn: Sequence[Callable[[Country], Dict]],
            save_as_json: bool = False
            ):
        
        if not wanted_tags:
            raise ValueError(none_wanted_tag_error)
        if not metrics_fn:
            raise ValueError(empty_seq_metrics_fn_error)
        
        CountryManager.wanted_tags = wanted_tags    # set varclass tags for runtime
        
        self.wanted_tags = wanted_tags
        self.metrics_fn = metrics_fn
        self._cache_files_as_json = save_as_json

        folder_path = Path(folder_path)
        self._files_generator = list(folder_path.iterdir())

        # initialisate runtime parsing
        self._parse_files()
        self.metrics_df = self._get_df_long_from_files()
    

    def __repr__(self) -> str:
        return repr(self.metrics_df)

    def _parse_files(self):
        """ 
        Iterates all found files in the defined folder and returns 
        the defined metrics in each file
        """
        save_metrics = []

        for filepath in self._files_generator:

            if filepath.is_file():

                vic3_reader = Vic3Reader(filepath, use_json=True)
                data = vic3_reader.data
                # Save as JSON in disk if flagged
                if self._cache_files_as_json:
                    vic3_reader.save_as_json(data, override=False)
                
                save_metrics.append(
                    SaveMetrics(
                            data, 
                            self.wanted_tags, 
                            self.metrics_fn
                        ).to_dataframe() + (filepath,)
                )  # add tuple from .to_dataframe and path of file for traceability

        # sort at the end by saved date
        self._saved_metrics: List[ Tuple[date, pd.DataFrame] ] = sorted(save_metrics, key=lambda x: x[0])


    def _get_df_long_from_files(self):
        """
        Merge multiple (game_date, df) tuples into one dataframe.
        It is expected that each dataframe has Tag ids as index and metrics as columns.
        
        Result: MultiIndex (game_date, tag_id) dataframe with variables as columns.
        This dataframe is in long format.
        """
        dfs = []

        for game_date, df, filepath in self._saved_metrics:

            index_name = "tag_id"
            if df.index.name != index_name:
                df = df.set_index(index_name, drop=True)

            # Add date to index
            df.index = pd.MultiIndex.from_product(
                [[game_date], df.index],
                names = ["game_date", index_name]
            )
            dfs.append(df)

        merged_df = pd.concat(dfs)  # along rows
        return merged_df

    def save_long(self, filename: str, folder: str = None, **kwargs):
        """
        Save dataframe to disk in various formats.
        The format is inferred from the file extension.
        Extra kwargs are passed to the corresponding pandas method.
        """
        # Extract file extension without dot and convert to lowercase
        ext = Path(filename).suffix[1:].lower()

        if not ext:
            raise ValueError("Filename must have an extension to infer the format.")
        
        if folder:
            folder_path = Path(folder)
            folder_path.mkdir(parents=True, exist_ok=True)
            filepath = folder_path / filename

        # Construct the method name
        method_name = f"to_{ext}"

        # Check if the dataframe has this method
        if not hasattr(self.metrics_df, method_name):
            raise ValueError(f"Unsupported file format: {ext}")

        # Dynamically call the method
        kwargs['index'] = True
        getattr(self.metrics_df, method_name)(filepath, **kwargs)


    def save_multiple_sheets(self, filename: str, folder: str = None, **kwargs ):
        """
        Save dataframe to disk as a spreadsheet with a sheet per variable: xlsx, xls or ods.
        The format is inferred from the file extension.
        Extra kwargs are passed to the corresponding pandas method.
        """
        # Extract file extension without dot and convert to lowercase
        ext = Path(filename).suffix[1:].lower()

        if not ext or ext not in ['xlsx', 'xls', 'ods']:
            raise ValueError("Filename must have a valid extension to support sheets: xlsx, xlsx or ods.")
        
        if folder:
            folder_path = Path(folder)
            folder_path.mkdir(parents=True, exist_ok=True)
            filepath = folder_path / filename

        wide_tables: Dict[str, pd.DataFrame] = {}

        for col in self.metrics_df.columns:
            wide_tables[col] = self.metrics_df[col].unstack(level='tag_id')

        kwargs['index'] = True

        with pd.ExcelWriter(filepath, engine=kwargs.get('engine', None)) as writer:
            for var, table in wide_tables.items():
                table.columns = table.columns.map(str)  # avoid excel reinterpreting the IDs as floats
                table.to_excel(writer, sheet_name=var, **kwargs)
    

class SaveMetrics():
    """
    Object specialised in extrating the defined metrics from one vic3 save file. 

    Parameters:
    -   data: Dict or Vic3save.Save file information as a Dict or already validated in Pydantic object.

        If a Dict object is given, the class already implements the validation of the data.

    -   wanted_tags: Tag IDs of countries whose metrics will be extracted.

        This ensures efficient computation, overlooking unwanted countries.

    -   metrics_fn: Iterable sequence i.e. List, of functions designed to accept a Vic3save data model and return 
                    a dictionary with a set of metrics. This controls the metrics that will be extracted from the file.

    Methods:
    -   to_dataframe(). Use this method to parse all extracted metrics to a dataframe object. This returns a tuple with the
        table and the date in the game.
    """
    def __init__(
            self, 
            data: Dict | Vic3Save, 
            wanted_tags: Set[TagIDStr],
            metrics_fn: Sequence[Callable[[Country], Dict]]
            ):
        
        if not wanted_tags:
            raise ValueError(none_wanted_tag_error)
        if not metrics_fn:
            raise ValueError(empty_seq_metrics_fn_error)
        
        if not isinstance(data, Vic3Save):
            try:
                data = Vic3Save(**data)
            except ValidationError as e:
               raise Vic3Save.pretty_missing_fields(e)
        
        self.data = data

        self.tags = wanted_tags
        
        self.metrics_fn: List[Callable[[Country], Dict]] = list(metrics_fn)
        self.metrics_fn.append(get_tag_data) # ensure the TAG is always extracted

    def _get_metrics_for_tag(self,
                        tag: TagIDStr,
                        ) -> Dict:

        merged = {}     # Warning: make sure there are not repeated keys

        for func in self.metrics_fn:
            merged.update(func(self.data, tag))

        return merged

    def _iterate_tags(self,
                     ) -> Dict:
        
        tags_metrics = {}

        for tag in self.tags:
            tags_metrics[tag] = self._get_metrics_for_tag(tag)
        
        return tags_metrics
    

    def to_dataframe(self, 
                     ) -> Tuple[date, pd.DataFrame]:
        """ 
        Construct Pandas DataFrame based on a dictionary of metrics
            where Dict is {tag id: metrics}
            and metrics is a Dict {metric name: value}

        Returns:
        -   TUPLE:
            -   date (save): date class
            -   pd.DataFrame with constructed stats for a given year.

            The returned dataframe shape is row: Tag id, column: metric.
        """
        tags_metrics = self._iterate_tags()

        metric = get_game_date(self.data.date)
        game_date = metric['game_date']

        return (
            game_date, 
            pd.DataFrame.from_dict(tags_metrics, orient='index').rename_axis("tag_id"),
        )
    
        # The dataframe contructed here is in the format tag_id as row index and metrics as columns