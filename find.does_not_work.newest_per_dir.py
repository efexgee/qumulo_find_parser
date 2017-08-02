#!/usr/bin/env python3

# Prints csv of entries that are newer that specified date
# Prints
#   date,user,group,file
# Expects the output of this find:
#   find 05_risk -printf "%y|%m|%u|%g|%AY-%Am-%Ad %AH:%AM|%CY-%Cm-%Cd %CH:%CM|%TY-%Tm-%Td %TH:%TM|%p\n"

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

DATE_OBJ = datetime.datetime.strptime(DATE, "%Y-%m-%d").date()

# Actually start doing stuff

input_file = open(INFILE, 'r')

most_recent = {}
cur_dir = ""

for line in input_file:
    f_type, perms, owner, group, t_access, t_meta, t_data, file_path = line.split('|')
    data_obj = datetime.datetime.strptime(t_data.split()[0], "%Y-%m-%d").date()

    #split timestamps into date and time because we don't care about time granularity
    access_date, access_time = t_access.split(" ")
    metadata_date, metadata_time = t_meta.split(" ")
    data_date, data_time = t_data.split(" ")

    full_path = file_path.rstrip()

    if f_type == "d":
        # we're in a new directory
        if len(full_path) > len(cur_dir):
            # we went deeper down the directory tree
            cur_dir = full_path
            most_recent[cur_dir] = data_obj
            #print("cur dir",cur_dir)
        else:
            # we're done with this dir so print most recent
            print("Newest", most_recent[cur_dir], cur_dir)

    if data_obj > most_recent[cur_dir]:
        most_recent[cur_dir] = data_obj

    if data_obj > DATE_OBJ:
        #print(t_data, " ".join(file_path).rstrip())
        #print only files, because changed dirs without changed files are not interesting
        #if f_type == "f":
            #leaving spaces in group names b/c we a using fixed width columns in Excel, not seps
            #print(",".join([data_date, owner, group, " ".join(file_path).rstrip()]))
        #print(",".join([data_date, owner, group, full_path]))
        #print("Newest", most_recent[cur_dir], cur_dir)
        pass
