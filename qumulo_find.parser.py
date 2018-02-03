#!/usr/bin/env python3

#find 05_risk -printf "%y|%m|%u|%g|%AY-%Am-%Ad %AH:%AM|%CY-%Cm-%Cd %CH:%CM|%TY-%Tm-%Td %TH:%TM|%p\n"

import datetime
import sys

# CONSTANTS
REQ_ARGS = 2
DEBUG = False

# FUNCTIONS
def print_usage(command):
        print()
        print("Usage:", command, "<find_output_file> YYYY-MM-DD")

# CODE

# Grab script name for error messages and number of args
script_name = sys.argv[0]


# Check for the required number of arguments
num_args = len(sys.argv) - 1

if num_args != REQ_ARGS:
        print("Error:", script_name, "- Incorrect number of arguments:", num_args, "( Need",REQ_ARGS,")")
        print_usage(script_name)
        sys.exit()


# Grab all the arguments
INFILE = sys.argv[1]
DATE = sys.argv[2]

if DEBUG:
        print("DEBUG: INFILE =", INFILE)
        print("DEBUG: DATE   =", SHEET_NAME)

DATE_OBJ = datetime.datetime.strptime(DATE, "%Y-%m-%d").date()

# Actually start doing stuff

input_file = open(INFILE, 'r')

for line in input_file:
	f_type, perms, owner, group, t_access, t_meta, t_data, *file_path = line.split('|')
	access_obj = datetime.datetime.strptime(t_access.split()[0], "%Y-%m-%d").date()
	meta_obj = datetime.datetime.strptime(t_meta.split()[0], "%Y-%m-%d").date()
	data_obj = datetime.datetime.strptime(t_data.split()[0], "%Y-%m-%d").date()

	if data_obj > DATE_OBJ:
		print(t_data, " ".join(file_path).rstrip())
	#	print("Newer:", t_data, " ", " ".join(file_path).rstrip())
	#else:
	#	print("Older:", t_data, file_path)
