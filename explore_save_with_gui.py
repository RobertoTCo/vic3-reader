""" You can use this script to visualise a save game with a interactive interface."""

from pathlib import Path
from utils import create_gui
from parser.reader import Vic3Reader

FOLDER = 'saves/'
FILENAME = '...'


if __name__ == '__main__':

    filepath = Path(FOLDER) / FILENAME 

    vic3_reader = Vic3Reader(filepath, use_json=True)

    create_gui(vic3_reader.data)