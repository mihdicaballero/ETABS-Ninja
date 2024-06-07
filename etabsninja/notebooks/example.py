import sys
import os
from icecream import ic
# Get the current working directory
print(2+2)
current_folder = os.getcwd()
# Go up two directories
parent_folder = os.path.dirname(os.path.dirname(current_folder))
# Append the parent folder to the system path (for .ipynb files)
sys.path.append(parent_folder)
from etabsninja.interface import connect_to_etabs, test_etabs_connection
# Run this one time and that's it
SapModel,EtabsObject = connect_to_etabs()
test_etabs_connection()