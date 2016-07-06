#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search a directory for duplicate files.

:author: Dominik Lang
"""
import argparse
import hashlib
import itertools
import os


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='The directory in which to search for duplicates.')
    args = parser.parse_args()
    return args


def build_stats(directory):
    """Analyse the files in `directory` and create signatures."""
    try:
        paths = os.listdir(directory)
    except FileNotFoundError as e:
        return [], [(os.path.abspath(directory), e)]
    # else:
    old_cwd = os.getcwd()
    try:
        os.chdir(directory)
        files, errors = [], []
        for path in paths:
            try:
                if os.path.isfile(path):
                    files.append((os.path.abspath(path), _stat(path), _hash(path)))
            except Exception as e:
                errors.append((os.path.abspath(path), e))
    finally:
        os.chdir(old_cwd)
    return files, errors


def _stat(file_name):
    """Retrieve file size and modification time from the file system."""
    stat = os.lstat(file_name)
    return stat.st_size, stat.st_mtime


def _hash(file_name):
    """Create an MD5 hash from a file's content."""
    with open(file_name, 'rb') as file:
        hasher = hashlib.md5()
        data = file.read()
        hasher.update(data)
        return hasher.digest()


def identify_duplicates(stats):
    """Search the file signatures for duplicates."""
    if not stats:
        return
    # else:
    stats.sort(key=lambda t: (t[2], t[1]))
    # right now, only group by the file's hash. Include length later:
    grouped = itertools.groupby(stats, lambda t: t[2])
    for _, group in grouped:
        group = list(group)
        if len(group) > 1:
            for dupe in group[1:]:
                yield dupe


def process_duplicates(dupes):
    """Print the duplicates' paths to the standard output."""
    dupes = list(dupes)
    if dupes:
        print('Duplicates:')
        for dupe in dupes:
            print('  ', dupe[0])


def main():
    """Search for duplicates in a directory given as a CLI argument."""
    print("Working directory is '{}'".format(os.getcwd()))
    args = parse_arguments()
    print("Searching for duplicates in '{}'".format(os.path.abspath(args.dir)))
    stats = build_stats(args.dir)
    if stats[1]:
        print('Errors:')
        for error in stats[1]:
            print("  {}: '{}'".format(error[1].__class__.__name__, error[0]))
    dupes = identify_duplicates(stats[0])
    process_duplicates(dupes)


if __name__ == '__main__':
    main()
