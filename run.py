#!/usr/bin/env python3

import argparse

from main.main import QuailCompression
from analyse import analyse

parser = argparse.ArgumentParser(description="My Compression Tool")
parser.add_argument("-c", "--compress", help="File to compress")
parser.add_argument("-e", "--expand", help="Expand target file")
parser.add_argument("-o", "--output", help="Output filename")

args = parser.parse_args()

if args.compress:
    file_to_compress = args.compress
    f = open(file_to_compress)
    content = f.read()
    f.close()

    bit_str = QuailCompression.encode(content)
    
    if args.output:
        storage_file = args.output
        QuailCompression.write(storage_file, bit_str)

if args.expand:
    file_to_expand = args.expand
    
    content = QuailCompression.read(file_to_expand)
    decoded = QuailCompression.decode(content)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(decoded)
    
    else:
        print(decoded)
        