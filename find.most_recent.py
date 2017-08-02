#!/usr/bin/env python3

# Prints csv of entries that are newer that specified date
# Prints
#   date,user,group,file
# Expects the output of this find:
#   find 05_risk -printf "%y|%m|%u|%g|%AY-%Am-%Ad %AH:%AM|%CY-%Cm-%Cd %CH:%CM|%TY-%Tm-%Td %TH:%TM|%p\n"

import datetime
import sys

# CONSTANTS
REQ_ARGS = 1
DEBUG = False

# FUNCTIONS
def print_usage(command):
        print()
        print("Usage:", command, "<find_output_file>")
        print("")
        print("      ", "find . -printf '%y|%m|%u|%g|%AY-%Am-%Ad %AH:%AM|%CY-%Cm-%Cd %CH:%CM|%TY-%Tm-%Td %TH:%TM|%p'")

# CODE

# Grab script name for error messages and number of args
script_name = sys.argv[0]

# Check for the required number of arguments
num_args = len(sys.argv) - 1

if num_args != REQ_ARGS:
        print("Error: Incorrect number of arguments:", num_args, "( Need",REQ_ARGS,")")
        print_usage(script_name)
        sys.exit()

# Grab all the arguments
INFILE = sys.argv[1]

# Actually start doing stuff

input_file = open(INFILE, 'r')

most_recent = datetime.date.min

for line in input_file:
    f_type, perms, owner, group, t_access, t_meta, t_data, file_path = line.split('|')
    data_obj = datetime.datetime.strptime(t_data.split()[0], "%Y-%m-%d").date()

    #split timestamps into date and time because we don't care about time granularity
    data_date, data_time = t_data.split(" ")

    #remove newline
    full_path = file_path.rstrip()

    if data_obj > most_recent:
        most_recent = data_obj
        most_recent_path = full_path
        most_recent_line = line
        if DEBUG:
            print("Updated most recent:", data_obj)

if DEBUG:
    print("Most recent =", most_recent)
    print("Most recent path =", most_recent_path)

print(line)
