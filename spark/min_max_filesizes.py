# -----------------------------------------------------------------------------
# Author: cgarcia
# About: This goes through a set of directories and outputs the min and max sizes
# Usage: > spark-submit min_max_filesizes.py <results output file> <input dir. 1> <input dir. 2> ...
# -----------------------------------------------------------------------------

from os import sys, path, listdir

# Check input args and print usage instructions if incorrect.
if len(sys.argv) < 3:
	print('\nUsage: > min_max_filesizes.py <results output file> <input dir. 1> <input dir. 2> ...\n\n')
	exit(-1)

# Write a text file	
def write_file(text, filename):
	f = open(filename, "w")
	f.write(text)
	f.close()

# For a given filename, this updates the current minmax pair ((<some file>, <current min size>), (<some file>, <current max size>))
def update_minmax(filename, minmax):
	minv, maxv = minmax
	file_length = path.getsize(filename) # Get the file's size
	if minv == None or file_length < minv[1]: # Update min file size if needed
		minv = (filename, file_length)
	if maxv == None or file_length > maxv[1]: # Update max file size if needed
		maxv = (filename, file_length)
	return (minv, maxv)

# Read in command line args
input_dirs = sys.argv[2:] # Get all input directories
output_file = sys.argv[1] # Get the desired name of output file where results go

minmax = (None, None) # Holds the min and max-sized files - initialize to empty.

# Loop through each directory: 
for input_dir in input_dirs:
	# Select only files (not directories)
	onlyfiles = [f for f in listdir(input_dir) if path.isfile(path.join(input_dir,f))]
	onlyfiles = map(lambda f: path.join(input_dir, f), onlyfiles) # add dir. path to make full filename
	for f in onlyfiles: # Update min/max file sizes if needed based on the current file
		minmax = update_minmax(f, minmax)

# Below create the output report string
minv, maxv = minmax		
print(minmax)
report = "Smallest File: " + str(minv[0]) + " (" + str(minv[1]) + " bytes)\n" + "Largest File: " + str(maxv[0]) + " (" + str(maxv[1]) + " bytes)\n"
write_file(report, output_file)

