#!/usr/bin/env python3

import argparse

from main.main import QuailCompression
from analyse import analyse

parser = argparse.ArgumentParser(description="Quail Compression is a simple compression tool for ASCII-ext")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

extract_parser = subparsers.add_parser("extract", help="Extract a file")
extract_parser.add_argument("filename", help="The file to extract")
extract_parser.add_argument("-o", "--output", help="Output filename")
extract_parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")

compress_parser = subparsers.add_parser("compress", help="Compress a file")
compress_parser.add_argument("-o", "--output", help="Output filename")
compress_parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
compress_parser.add_argument("filename", help="The file to compress")

args = parser.parse_args()


if args.command == "compress":
    if not args.quiet:
        print(f"Compressing {args.filename}...")
        
    with open(
        args.filename
    ) as f:
        bit_str = QuailCompression.encode(f.read())

    QuailCompression.write(
        args.output if args.output else args.filename + ".qc",
        bit_str
    )
    
    if not args.quiet:
        print(f"Compressed into {args.output if args.output else args.filename + ".qc"}...")



elif args.command == "extract":
    if not args.quiet:
        print(f"Extracting {args.filename}...")
    
    decoded = QuailCompression.decode(
        QuailCompression.read(args.filename)
    )
    
    with open(args.output if args.output else "a.txt", "w") as f:
        f.write(decoded)
    
    if not args.quiet:
        print(f"Extracted into {args.output if args.output else "a.txt"}")
    

    