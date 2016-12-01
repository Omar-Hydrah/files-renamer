import os
import re
import time
import sys
import argparse

def main(argv): #{
	
	print('Welcome to the files renamer by Omar Hydrah');
	print('http://www.github.com/Omar-Hydrah/files-renamer\n');

	mode = '';
	path = '';
	# A flag to determine how the user started the program.
	# It will be set to True, if the user's started the program using command line arguments.
	command_line_args = False;

	def quit_program(message =''): #{
		if message == '': #{
			print('Problem occurred with the program. Please restart')
		#}
		elif message != '': #{
			print(message)
		#}
		sys.exit()
	#}

	# Register the user's target path
	# @return : path
	def prompt_for_path(): #{

		path = input("Enter a valid directory: \n")
		if not os.path.isdir(path): #{
			print('You supplied an invalid directory.')
			return prompt_for_path()
		#}

		elif os.path.isdir(path): #{
			os.chdir(path)
			return path
		#}
	#}	

	# The mode on which the program will run.
	# If it's regex, then the user will enter his own regex.
	# If it's renaming, then this is suited for multiple files than contain a unified  prefix or suffix
	# If it's singluar, then the user will be prompted to rename the files one file at a time
	# ---
	# @param regex | renaming | singular
	def prompt_for_mode(): #{

		mode = input('\nSelect your mode(singular, search, regex)');
		if mode == 'regex' or mode == 'search' or mode == 'singular': #{
			return mode
		#}
		else:
			return prompt_for_mode()
		#}
	#}


	# Displays all of the files in a path.
	#
	# @param : valid path
	# 
	# @return: void
	
	def display_path_files(path): #{
		if os.path.isdir(path): #{
			print('\nDirectory Content: ')
			
			for file_name in os.listdir(path): #{
				print(file_name)
				time.sleep(0.3)
			#}
		#}
		else: #{
			quit_program('This is not a valid directory.');
		#}
	#}

	# Check if the currently declared mode is valid (regex, search, singular)
	def check_mode(mode): #{
		if mode != 'singular' and mode != 'regex' and mode != 'search': #{
			return False;
		#}
		else: #{
			return True;
		#}
	#}

	parser = argparse.ArgumentParser();
	parser.add_argument('-m', '--mode', help='The mode of renaming. (singular, search, regex)');
	parser.add_argument('-p', '--path', help='The directory that contains the files to be renamed.');
	arguments = parser.parse_args();


	if arguments.path and arguments.mode: #{
		if not check_mode(arguments.mode): #{
			quit_program('Unrecognized mode.');
		#}

		if not os.path.isdir(arguments.path): #{
			quit_program('Invalid path.');
		#}
		mode = arguments.mode;
		path = arguments.path;
		os.chdir(path);
		command_line_args = True;

	#}
	else: #{
		path = prompt_for_path();
	#}


	display_path_files(path);

	# If command line arguments were not provided, then the user does not have a mode selected.
	if not command_line_args: #{
		print('______________')
		print('Renaming modes:')
		# Singular mode
		print('-singular: Change file names one at a time manually')
		time.sleep(0.2)
		# Renaming mode
		print("-search: Search a common part in file names, and replace it")
		time.sleep(0.2)
		# Regular Expressions mode.
		print("-regex: Enter a regular expression, and the replacement for found matches", end='\n') 
		time.sleep(0.2);

		mode = prompt_for_mode()
	#}


	# Ask the user for a regular expression, and the subsitution for found matches.
	# @return list [regex, regex_sub]
	def prompt_for_regex():
		# print('Enter your regular expression:')
		regex     = input('Enter your regular expression:\n')
		# print('Enter substitution for found matches.')
		regex_sub = input('The replacement for found matches:\n')
		return [regex, regex_sub]


	# Ask the user for a common part, and the replacement for found matches.
	def prompt_for_search():
		print('Enter your search term:')
		common_part = str(input())
		print('The replacement:')
		replacement   = str(input())
		return [common_part, replacement]

	# Ask the user to confirm renaming
	def confirm_renaming():
		choice = input('Go ahead and rename?(yes, no)\n')
		if choice == 'yes':
			return choice
		elif choice == 'no':
			print('Restart the program')
			sys.exit()
		else:
			return confirm_renaming()

	# Found matches for the regex, will be replaced.
	if mode == 'regex':
		regex_prompt = prompt_for_regex()
		if len(regex_prompt) != 2:
			# A problem occurred
			quit_program()

		regex = regex_prompt[0]
		regex_sub = regex_prompt[1]


		pattern = re.compile(regex)

		# A list containing all found files, with absolute paths
		regex_found_files = []

		print('new names will be: ')
		for file_name in os.listdir(path):
			if pattern.search(file_name):

				time.sleep(0.3)
				print(re.sub(regex, regex_sub, file_name))
				regex_found_files.append(os.path.abspath(file_name))


		# If the user chooses "no", the program will terminate
		# If the user chooses "yes", the program will continue	
		confirm_renaming()
		for file in regex_found_files:
			new_name = re.sub(regex, regex_sub, file)
			os.rename(file, os.path.abspath(new_name));

		print('Renaming complete')



	# -----------------------------------------------
	# A common string will be replaced from all files
	# -----------------------------------------------
	if mode == 'search':
		search_prompt = prompt_for_search()
		if len(search_prompt) != 2:
			# A problem occurred
			quit_program()

		common_part = search_prompt[0]
		replacement = search_prompt[1]

		# A list containing absolute paths of files that match the search term
		replacement_found_files = []
		print('New names: ')
		for file_name in os.listdir(path):
			if common_part in file_name:
				replacement_found_files.append(os.path.abspath(file_name))
				print(file_name.replace(common_part, replacement))

		# If the user chooses "no", the program will terminate
		# If the user chooses "yes", the program will continue
		confirm_renaming()
		for file in replacement_found_files:
			new_name = file.replace(common_part, replacement)
			os.rename(file, new_name)
			print(new_name)

		print('Renaming complete')

	# 
	# Files will be renamed one by one
	if mode == 'singular':
		print('You will change every file manually. You can leave the extension out.')
		time.sleep(0.5)
		print('No file will be affected if you press enter')
		time.sleep(0.5)
		print('Rename with caution. This process can not be undone\n')
		time.sleep(0.5)
		for file_name in os.listdir(path):
			if not '.' in file_name: #{
				continue;
			#}
			extension = os.path.splitext(file_name)[1]
			print(file_name)
			new_name = input('New name: ')

			if new_name == '':
				continue
			elif extension in new_name:
				# The user supplied the extension.
				os.rename(file_name, os.path.abspath(new_name))
			else:
				os.rename(file_name, os.path.abspath(new_name + extension))

		print('Renaming complete.')
				
#}
if __name__ == '__main__':#{
	try: #{
		main(sys.argv);
	#}
	except KeyboardInterrupt: #{
		print('\nSalam');
	#}
#}
