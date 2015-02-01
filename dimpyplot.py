#!/usr/bin/env python

import subprocess

def dimplot(filename):
	"""Emulates running the LigPlot+ DIMPLOT algorithm. Rewriting as a CLI to allow for a batch mode."""
	file_prefix = filename.strip('.pdb')[0]

	# Run HBadd
	subprocess.check_call(['hbadd', filename,
	'/Applications/LigPlus/lib/params/components.cif', # change this line to match your components.cif location
	'-wkdir', './'], shell = False)


	# Run HBplus
	subprocess.check_call(['hbplus', '-L', '-h', '2.90', '-d', '3.90', '-N', filename, '-wkdir', './'], shell = False)


	# Run HBplus again
	subprocess.check_call(['hbplus', '-L', '-h', '2.70', '-d', '3.35', filename, '-wkdir', './'], shell = False)


	# Run dimer
	subprocess.check_call(['dimer', filename, 'A', 'C'], shell = False)


	# Run dimhtml
	subprocess.check_call(['dimhtml', 'none', '-dimp', '-dir', './', '-flip', '-ctype', '1'], shell = False)


	# Run ligplot
	subprocess.check_call([
		'ligplot', 'dimplot.pdb', '-wkdir', './',
		'-prm', '/Applications/LigPlus/lib/params/dimplot.prm', '-ctype', '1'
		], shell = False)


	# Rename trashy files
	files_to_rename = [_ for _ in subprocess.check_output(['ls']).split('\n') if
		'dimplot.' in _[0:8] or 'ligplot.' in _[0:8]]

	for file_to_rename in files_to_rename:
		subprocess.check_call([
			'mv',
			file_to_rename,
			'./{}.{}'.format(filename.split('.pdb')[0], file_to_rename)
			])

def main():
	"""Main function."""
	# Get list of pdb files in the directory
	pdb_files = [_ for _ in subprocess.check_output(['ls']).split('\n') if
		_[-4:] == '.pdb' and 'dimplot' not in _ and 'ligplot' not in _]
	for pdb_file in pdb_files:
		dimplot(filename=pdb_file)
	quit()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n\nGoodbye!\n\n')