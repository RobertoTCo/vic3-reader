""" Define here all the variables to configure what metrics, which files and how to use the vic3-reader tool."""
# What is the folder to the save vic3 files?

FOLDER_SAVES = 'saves/'


# Which format and where you want to save the results? 
# The file extension needs to be valid for pandas (excel, ods, csv, parquet, feather, json, html, ...)
# see https://pandas.pydata.org/pandas-docs/stable/search.html?q=to_

FOLDER_RESULTS = 'results/'
FILE_RESULTS = "results.csv"


# If you are running through the same files multiple times, you may want to set this as True to save time
# Warning! Vic3 saves as JSON are around 500MB, be careful with your disk space
CACHE_AS_JSON = False


# Define what metrics you want to extract importing the main functions
# from the 'metrics' modules

from vic3_reader.metrics import get_adm, get_economy

METRICS = [
    get_economy,
    get_adm,
]


# Define which countries you want to get the metrics from

# Hint: If you are not sure about the Tag IDs (numeric), you can explore the 
# a plain-text save searching for "definition=" or use or 

TAGS = [
    "1",      # GBR
    "3",      # RUS
    "4",      # FRA
    "5",      # PRU, evolves to NGF, GER
    "8",      # AUS, evolves to HAB
    "9",      # USA
    "17",     # JAP
    "23",     # SWE
    "29",     # NET
    "36",     # SPA
    "62",     # SAR, can evolve to ITA
    "94",     # TUR
    "199",    # BRZ
]
