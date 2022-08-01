# analyze_grains.py
#
# This is a chunk of code to read  machine data (.dat and .raw files) and yield 
# a 3d array of intensity values.
#
# summer 2022, Matthew Ellison (matthew.ellison.gr@dartmouth.edu)
#
# adapted from code written in summer 2021 

import sys
import os
import pickle
import xml.etree.ElementTree as ET
import numpy as np
from datetime import datetime

#helper functions for interface
def banner_string(line_text, symbol = '-'):
	n = len(line_text)
	out = ""
	out += n * symbol + '\n'
	out += line_text + '\n'
	out += n * symbol
	return out

break_line = "-----------------------------"
class Log():
	def __init__(self, log_name):
		self.log = open(log_name, 'a')
		self.log_line(break_line)
	def log_line(self, line_text):
		self.log.write('(' + str(datetime.now()) + ')' + line_text + '\n')
	def close(self):
		self.log_line(break_line)
		self.log.close()	
def input_until_type(text, type):
	while True:
		response = input(text)
		try:
			return type(response)
		except:
			print("invalid input, please try again.")
			continue

def input_until_condition(text, condition):
	while True:
		response = input(text)
		if condition(response):
			return response
		else:
			print("invalid input, please try again.")

def input_choice_from_list(initial_message, array):
	print(initial_message)
	for i, item in enumerate(array):
		print('\t', str(i) + '.', item)
	response = input_until_condition("which would you like?(0-" + str(len(array) - 1) + ") ", lambda x: x in map(str, range(len(array)))) 
	return array[int(response)]

#actual parsing code
def parse_dat_file(dat_file, log):		
	'''
	pick out desired components of dat xml file. should be formatted like sample dat file.
	on error parsing the file, falls back on user input of values.
	returns a dictionary with values for the following keywords:
		> "dimensions" : a 3-tuple (#rows, #cols, #layers) (i.e. x_dim, y_dim, z_dim)
		> "spacings" : a 3-tuple (row_spacing, col_spacing, layer_spacing) 
	'''
	out_dict = dict()
	try: #try parsing as xml
		tree = ET.parse(dat_file)
		root = tree.getroot()
		for child in root:
			if child.tag == "Resolution":
				raw_tuple = (child.attrib['X'], child.attrib['Y'], child.attrib['Z'])
				out_dict["dimensions"] = tuple(map(int, raw_tuple))
			elif child.tag == "Spacing":
				raw_tuple = (child.attrib['X'], child.attrib['Y'], child.attrib['Z'])
				out_dict["spacings"] = tuple(map(float, raw_tuple))
			else:
				pass
	except: #otherwise fall back on user input
		response = input_until_condition("error parsing dat file "  + dat_file + ". Would you like to manually enter the values (y/n)? ", lambda x: x in ['y', 'n'])	
		if response == 'n':
			print("ok, exiting program")
			log.close()
			exit()
		else: #response is 'y'
			dimension_info = []
			dimension_info.append(input_until_type("number of rows? ", int))
			dimension_info.append(input_until_type("number of columns? ", int))
			dimension_info.append(input_until_type("number of layers? ", int))
			out_dict["dimensions"] = tuple(dimension_info)

			spacing_info = []
			spacing_info.append(input_until_type("row spacing? ", float))
			spacing_info.append(input_until_type("column spacing? ", float))
			spacing_info.append(input_until_type("layer spacing? ", float))
			out_dict["spacings"] = tuple(spacing_info)	
	return out_dict

def unpack_raw_file(raw_file_path, dat_file_dict, log, verbose = False):
	'''
	unpacks the raw file, returning either
		1. "failed" on error
		2. data as a numpy 3darray on success
	asks the user to assist along the way
	'''
	#infer encoding from file size
	try:
		num_bytes = os.path.getsize(raw_file_path)
		dims = dat_file_dict["dimensions"]
		array_size = dims[0] * dims[1] * dims[2] 
		bits_per_entry = (num_bytes * 8) / array_size
		#get closest smaller power of 2
		current = 1
		while current < bits_per_entry:
			current *= 2
		if verbose:
			print("Inferred encoding of raw file is 'uint" + str(current) + "'", "(i.e. grayscale 0-" + str(2 ** current - 1) + ')')
			response = input_until_condition("Does that seem reasonable?(y/n) ", lambda x: x in ['y', 'n'])	
		else:
			response = 'y'
		if response == 'y':
			encoding = 'uint' + str(current)
		else: #'n'
			response = input_until_condition("Would you like to enter a corrected encoding in a moment?(y/n) ", lambda x: x in ['y', 'n'])
			if response == 'n':
				print("ok, aborting command")
				return "failed"
			else: #'y'
				response = input("ok, please enter a corrected data type: ")
				encoding = response	
	except: #file not found / inaccessible
		print("error accessing raw file", "'" + raw_file_path + "'")
		response = input_until_condition("Would you like to enter a corrected path in a moment?(y/n) ", lambda x: x in ['y', 'n'])
		if response == 'n':
			print("ok, aborting command")
			return "failed"
		else: #'y'
			response = input("ok, please enter a corrected path: ")
			return unpack_raw_file(response, dat_file_dict, log)
	log.log_line("attempting to unpack raw file " + raw_file_path + "'"" with encoding " + "'" + encoding + "'")
	#now unpack	
	try:
		data = np.fromfile(raw_file_path, dtype=encoding)	
		dims = dat_file_dict["dimensions"]
		data = data.reshape(dims[2], dims[1], dims[0]) #layers, rows, columns		
		log.log_line("success")
		return data
	except:
		log.log_line("failed")	
		response = input_until_condition("Unpacking failed. Try again, maybe with different encoding?(y/n) ", lambda x: x in ['y', 'n'])	
		if response == 'n':
			print("ok, aborting command")
			return "failed"
		else: #'y'
			print("ok, restarting command")
			return unpack_raw_file(raw_file_path, dat_file_dict, log)

#interface
def get_3d_array(raw_file_path, dat_file_path):
	log = Log("log.txt")	
	dat_data_dict = parse_dat_file(dat_file_path, log)
	big_array = unpack_raw_file(raw_file_path, dat_data_dict, log)
	return big_array	
