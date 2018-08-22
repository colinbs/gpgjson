# gpgjson.py
# Imports
import subprocess
import sys
import re
import json
import argparse

# Variables
raw_output = ""
all_keys = list()

current_key = dict()
current_key["pub0"] = dict()
current_key["sub0"] = dict()
next_is_fprint = False
curr_state = "pub"
index = 0
state_index = 0

# Args Parsing
parser = argparse.ArgumentParser()

parser.add_argument("keys", nargs='*',
                    help="The fingerprints of one or more keys.")
parser.add_argument("-a", "--all-keys", help="Print all GPG keys.",
                    action='store_true')
parser.add_argument("-i", "--indent", help="Indention of the JSON output.",
                    type=int, default=4)
parser.add_argument("-o", "--outfile", nargs=1, type=str,
                    help="The output file where the JSON should be written to.")

args = parser.parse_args()

# Execute Command
if args.all_keys:
    process = subprocess.run(args=["gpg", "--list-keys"], capture_output=True)
    if process.returncode > 0:
        print("No fingerprints found!")
        sys.exit()
    raw_output = str(process.stdout.decode("utf-8"))
elif args.keys:
    process = subprocess.run(args=["gpg", "--list-key"] + args.keys, capture_output=True)
    if process.returncode > 0:
        print("No fingerprint matched a key!")
        sys.exit()
    raw_output = str(process.stdout.decode("utf-8"))
else:
    parser.print_help()
    sys.exit()

# Split Output
raw_output_lines = raw_output.split('\n')

for line in raw_output_lines:
    # Main Loop
    # Prepare Line
    line = list(filter(None, line.split(' ')))
    line = list(map(lambda l: re.sub(r"[\[\]]", "", l), line))
    line = list(filter(lambda l: l, line))

    # Store Key
    if len(line) == 0:
        if current_key["pub" + str(state_index)]:
            state_index += 1
            all_keys.append(current_key)
            next_is_fprint = False
            current_key = dict()
            current_key["pub" + str(state_index)] = dict()
            current_key["sub" + str(state_index)] = dict()
        continue

    # Header Lines
    if '/' in line[0] or '-' in line[0]:
        continue
    else:
        # Parse Pub and Sub
        if line[0] == "pub" or line[0] == "sub":
            curr_state = line[0] + str(state_index)
            current_key[curr_state]["alg"] = line[1]
            current_key[curr_state]["cdate"] = line[2]
            current_key[curr_state]["flags"] = line[3]
            current_key[curr_state]["exdate"] = line[5]
            next_is_fprint = True if line[0] == "pub" else False
            index = 0

        # Parse Uid
        elif line[0] == "uid":
            current_key[curr_state]["uid" + str(index)] = dict()
            current_key[curr_state]["uid" + str(index)]["trust"] = line[1]
            current_key[curr_state]["uid" + str(index)]["name"] = ' '.join(line[2:-1])
            current_key[curr_state]["uid" + str(index)]["email"] = line[-1]
            index += 1

        # Parse Fingerprint
        elif next_is_fprint:
            current_key["fprint"] = line[0]
            next_is_fprint = False




# Write File
if args.outfile:
    with open(''.join(args.outfile), 'w') as outfile:
        json.dump(all_keys, outfile, indent=args.indent)
else:
    print(json.dumps(all_keys, indent=args.indent))


