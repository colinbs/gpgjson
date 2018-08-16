#!/usr/bin/python

import os
import sys
import re
import json

input_fprint = ""
command = "gpg --list-keys"

all_keys = list()

current_key = dict()
current_key["pub0"] = dict()
current_key["sub0"] = dict()

next_is_fprint = False
curr_state = "pub"
index = 0
state_index = 0

if len(sys.argv) > 1:
    input_fprint = sys.argv[1]
    command = "gpg --list-key "

raw_output = os.popen(command + input_fprint).read()

raw_output_lines = raw_output.split('\n')

for line in raw_output_lines:
    line = list(filter(None, line.split(' ')))
    line = list(map(lambda l: re.sub(r"[\[\]]", "", l), line))
    line = list(filter(lambda l: l, line))

    if len(line) == 0:
        if current_key["pub0"]:
            all_keys.append(current_key)
            next_is_fprint = False
            current_key = dict()
            current_key["pub0"] = dict()
            current_key["sub0"] = dict()
        continue
        
    if '/' in line[0] or '-' in line[0]:
        continue
    else:
        if line[0] == "pub":
            curr_state = "pub" + str(state_index)
            current_key[curr_state]["alg"] = line[1]
            current_key[curr_state]["cdate"] = line[2]
            current_key[curr_state]["flags"] = line[3]
            current_key[curr_state]["exdate"] = line[5]
            next_is_fprint = True
            index = 0
        elif line[0] == "uid":
            current_key[curr_state]["uid" + str(index)] = dict()
            current_key[curr_state]["uid" + str(index)]["trust"] = line[1]
            current_key[curr_state]["uid" + str(index)]["name"] = ' '.join(line[2:-1])
            current_key[curr_state]["uid" + str(index)]["email"] = line[-1]
            index += 1
        elif line[0] == "sub":
            curr_state = "sub" + str(state_index)
            current_key[curr_state]["alg"] = line[1]
            current_key[curr_state]["cdate"] = line[2]
            current_key[curr_state]["flags"] = line[3]
            current_key[curr_state]["exdate"] = line[5]
            index = 0
        elif next_is_fprint:
            current_key["fprint"] = line[0]
            next_is_fprint = False

if command == "gpg --list-keys":
    filename = "all_keys.json"
if command == "gpg --list-key ":
    filename = input_fprint + ".json"

with open(filename, 'w') as outfile:
    json.dump(all_keys, outfile)
