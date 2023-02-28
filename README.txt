The project depends on these modules:

matplotlib.pyplot
matplotlib.path
numpy

Extract the project to a location accessible by Python and install dependencies.

To run the project open a terminal in the root directory and run the command 'python search.py'

A menu will prompt asking to specify which algorithm to run. Once a selection is made the graph will appear and summary information will be displayed in the console. Summary information can also be found in the summary.txt file and the .PNG files provided in the TestingGrid directory.

To choose another algorithm to run close the graph and rerun the program.

The project comes with 4 world files:
	
	world1_enclosures.txt
	world1_turfs.txt
	world2_enclosures.txt (Default)
	world2_turfs.txt (Default)

To configure the project to use different world files, change the parameter to the gen_polygons(...) function call in the search.py file.

Note: When adding new enclosures or turfs to the world1_enclosures.txt and world1_turfs.txt files, ensure exactly ONE blank line is present at the end of the file.