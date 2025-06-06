#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File Management CLI Tool
========================

This script provides a simple command‑line interface (CLI) for basic file operations:
  - list:     List all files and subdirectories in a given directory, showing their
              last modification time and size.
  - search:   Search for files whose names contain a given keyword.
  - copy:     Copy a file from a source path to a destination path.
  - version:  Display the tool’s version information.

Usage examples:
  $ python filetool.py list /path/to/dir
  $ python filetool.py search report .
  $ python filetool.py copy data.csv backup/data.csv
  $ python filetool.py --version
"""

Running in Warp Terminal:
1. Open Warp and navigate to the directory containing this script:
     ```bash
     cd /path/to/your/script
     ```
2. (Optional) Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies (none beyond Python standard library). If you still
   want to ensure argparse is available:
     ```bash
     pip install argparse
     ```
4. To list files in the current directory in a split pane, press Option+Enter to
   open a new pane and run:
     ```bash
     python filetool.py list .
     ```
5. To search for a keyword across files in a directory:
     ```bash
     python filetool.py search keyword /path/to/search
     ```
6. To copy a file from one location to another:
     ```bash
     python filetool.py copy source.txt destination.txt
     ```
7. Use Warp’s pane splitting, session search, and command palette to streamline
   repeated operations and review command history.

import os
import sys
import shutil
import time
import argparse

# Version information
VERSION = "1.0.0"

def list_files(directory='.') -> None:
    """
    List all files and directories in the specified directory.
    Shows each item’s type ([FILE] or [DIR]), name, last modified timestamp, and size in bytes.
    """
    print(f"Contents of directory: {directory}")
    try:
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            last_modified = time.ctime(os.path.getmtime(path))
            size = os.path.getsize(path)

            if os.path.isdir(path):
                print(f"[DIR]  {entry:30} {last_modified:30} {size:10} bytes")
            else:
                print(f"[FILE] {entry:30} {last_modified:30} {size:10} bytes")
    except Exception as e:
        print(f"Error listing directory '{directory}': {e}")

def search_files(keyword: str, directory='.') -> None:
    """
    Search for files in the given directory (and subdirectories) whose names contain the keyword.
    Prints each matching file’s path.
    """
    print(f"Searching for files containing '{keyword}' in: {directory}")
    found = False

    for root, _, files in os.walk(directory):
        for filename in files:
            if keyword.lower() in filename.lower():
                filepath = os.path.join(root, filename)
                print(f"Found: {filepath}")
                found = True

    if not found:
        print(f"No files found containing '{keyword}'.")

def copy_file(source: str, destination: str) -> None:
    """
    Copy a file from source to destination, preserving metadata.
    """
    try:
        shutil.copy2(source, destination)
        print(f"Copied: {source} -> {destination}")
    except Exception as e:
        print(f"Failed to copy '{source}' to '{destination}': {e}")

def show_version() -> None:
    """
    Print the tool’s version and copyright.
    """
    print(f"File Management CLI Tool v{VERSION}")
    print("Copyright (c) 2025")

def main() -> None:
    """
    Parse command‑line arguments and dispatch to the appropriate function:
      - list
      - search
      - copy
      - version (also via -v / --version)
    """
    parser = argparse.ArgumentParser(
        description="File Management CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'list' command
    list_parser = subparsers.add_parser("list", help="List files in a directory")
    list_parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to list (default: current directory)"
    )

    # 'search' command
    search_parser = subparsers.add_parser("search", help="Search for files by keyword")
    search_parser.add_argument("keyword", help="Keyword to search for in filenames")
    search_parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search (default: current directory)"
    )

    # 'copy' command
    copy_parser = subparsers.add_parser("copy", help="Copy a file")
    copy_parser.add_argument("source", help="Path to the source file")
    copy_parser.add_argument("destination", help="Destination path")

    # 'version' command
    subparsers.add_parser("version", help="Show version information")

    # Also allow -v / --version
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information and exit"
    )

    args = parser.parse_args()

    # If the version flag is present, show version and exit
    if args.version:
        show_version()
        return

    # Dispatch based on the subcommand
    if args.command == "list":
        list_files(args.directory)
    elif args.command == "search":
        search_files(args.keyword, args.directory)
    elif args.command == "copy":
        copy_file(args.source, args.destination)
    elif args.command == "version":
        show_version()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
