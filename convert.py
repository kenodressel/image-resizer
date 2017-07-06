import subprocess
import glob
import os
import re
import signal

PID_FILE = "/tmp/pictures.pid"

# handle ctrl + c
def signal_handler(signal, frame):
	global PID_FILE	
	os.remove(PID_FILE)
	sys.exit(0)


def is_folder(path, strict=True):
	if(strict):
		return os.path.isdir(path)
	else:
		if(not os.path.isdir(path)):
			os.mkdir(path)
		return True


def transform_filename(org_filename):
	parts = org_filename.split('.')
	name = ".".join(parts[:-1])
	ext = parts[-1]
	return name + '-compressed.' + ext

def get_all_convertables(o_folder, new_folder):

	types = ('*.jpg', '*.JPG', '*.png', '*.PNG')
	all_src = []
	all_trans = []
	process_files = []

	for t in types:
		src = glob.glob(o_folder + '/' + t)
		all_src.extend([os.path.basename(x) for x in src])

		trans = glob.glob(new_folder + '/' + t)
		all_trans.extend([os.path.basename(x) for x in trans])
	
	for s in all_src:
		n = transform_filename(s)
		if(n not in all_trans):
			process_files.append(s)

	return process_files

def transform_files(o_folder, new_folder, file_list):

	for f in file_list:
		bashCommand = "convert " + o_folder + '/' + f + " -resize 2048x -quality 50% " + new_folder + '/' + transform_filename(f)
		process = subprocess.call(bashCommand.split(), stdout=subprocess.PIPE)
		#output, error = process.communicate()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)

	if(os.path.isfile(PID_FILE)):
		# another version is still running
		print("ERR: Found PID file.")
		exit(0)
	else:
		open(PID_FILE, 'a').close()

	o_folders = ["./org"]
	new_folder = "./small"


	
	if(not is_folder(new_folder, False)):
		print("ERR: could not create new folder")
		os.remove(PID_FILE)
		exit(1)

	for o_folder in o_folders:
		# check folders
		if(not is_folder(o_folder)):
			print("ERR: original folder not found")
			os.remove(PID_FILE)
			exit(1)

		convertables = get_all_convertables(o_folder, new_folder)
		transform_files(o_folder, new_folder, convertables)

	os.remove(PID_FILE)
	exit(0)
