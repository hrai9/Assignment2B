#!/usr/bin/env python3

import subprocess, sys
import argparse

'''
OPS445 Assignment 2B | OPS445
Program: duim.py 
Author: "Harkarn Rai"
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script provides a disk usage summary using `du` command, 
presents it in human-readable format if specified, and generates bar charts 
to visualize the usage.

Date: <Date>
'''

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Display sizes in human-readable format.")
    parser.add_argument("target", nargs=1, help="Target directory to analyze.")
    args = parser.parse_args()
    return args

def percent_to_graph(percent: int, total_chars: int) -> str:
    "Returns a string representing a bar graph for the given percentage."
    filled_length = round((percent / 100) * total_chars)  # Round to nearest integer
    return "#" * filled_length + " " * (total_chars - filled_length)

def call_du_sub(location: str) -> list:
    "Use subprocess to call `du -d 1 <location>` and return raw list."
    try:
        result = subprocess.run(["du", "-d", "1", location], capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while running 'du': {e}")
        return []
    except FileNotFoundError:
        print(f"Error: The directory '{location}' does not exist.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for directory '{location}'.")
        return []



def create_dir_dict(raw_dat: list) -> dict:
    "Convert raw du output into a dictionary with directory sizes."
    dir_dict = {}
    for line in raw_dat:
        size, path = line.split("\t")
        dir_dict[path] = int(size)
    return dir_dict

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "Convert sizes from KiB to a human-readable format."
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    suf_count = 0
    result = kibibytes
    while result >= 1024 and suf_count < len(suffixes) - 1:
        result /= 1024
        suf_count += 1
    return f"{result:.{decimal_places}f} {suffixes[suf_count]}"

if __name__ == "__main__":
    args = parse_command_args()

    # Parse target directory
    target_dir = args.target[0]

    # Call du and process the output
    raw_output = call_du_sub(target_dir)
    dir_data = create_dir_dict(raw_output)

    # Calculate total size for percentages
    total_size = sum(dir_data.values())

    # Print results
    print(f"Disk Usage Report for {target_dir}")
    print("-" * 40)
    for directory, size in dir_data.items():
        percentage = (size / total_size) * 100
        graph = percent_to_graph(percentage, args.length)
        if args.human_readable:
            size_str = bytes_to_human_r(size)
        else:
            size_str = f"{size} KiB"
        print(f"{size_str:<10} {graph} {directory}")
