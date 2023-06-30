import sys
import os
from icecream import ic
# Get the current working directory
current_folder = os.getcwd()
# Append the current folder to the system path (for .py files)
sys.path.append(current_folder)

from etabsninja.interface import test_etabs_connection
# # Run this one time and that's it
# SapModel,EtabsObject = connect_to_etabs()  sdfsd

test_etabs_connection()