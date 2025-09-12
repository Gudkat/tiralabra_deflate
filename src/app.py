import sys
import random
from string import ascii_letters
from algorithms.huffman import Huffman

def output_help():
    print("""
The program requires bitarray to work. 
          
To install required dependencies with poetry use `poetry install`.

Usage:
    Use the app with poetry using `poetry run python app.py [options] [file_name]`

Options:
    -h                  Print this message and terminate.
    algorithm <str>     Selects the algorithm used for compression or decompression.
                        available algorithms: 
                            huffman
                            lz77        [CURRENTLY MISSING]
    -d                  Used to indigate to the program that we are decompressing the data. To compress the data, omit this flag.
Example how to compress data using the algorithm: 
    `poetry run python app.py algorithm huffman test_data`
""")
    exit()


def main(filename: str, encode: bool, algo=None):
    with open(filename, "r") as file:
        data = file.read()

    if algo == 'huffman':
        chosen_alorithm = Huffman()

    if not algo:
        print("no regocnizable algorithm entered")
        exit()

    ret = chosen_alorithm.encode(data)
    
    print(ret)


if __name__ == "__main__":
    implemented_algorithms = ['huffman']
    encode = True

    if "-h" in sys.argv or "help" in sys.argv:
        output_help()
    if "-d" in sys.argv:
        encode = False
    if "algorithm" in sys.argv:
        algo = (sys.argv[sys.argv.index("algorithm") + 1])
        if algo not in implemented_algorithms:
            print("Currently only the following compression algorithms are implemented")
            for algo in implemented_algorithms:
                print(" - " + algo)
            exit()
    
    filename = sys.argv[-1]
    
    main(filename, encode, algo)