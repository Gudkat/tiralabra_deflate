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
                            deflate     [CURRENTLY MISSING]
    -d                  Used to indigate to the program that we are decompressing the data. To compress the data, omit this flag.
    -g <int>            Number indicates how much test data is generated. The number is character to the power of the given argument.
                        For example command `poetry run python app.py -g 5` will generate 10**5 = 100 000 characters of test data in ASCII. This corresponds to little bit under = 100 kb of test data.
                        
                        Example: To save store the test data to file, use it like `poetry run python app.py -g 5 > test_data`
          
Example how to compress data using the algorithm: 
    `poetry run python app.py algorithm huffman test_data`
""")
    exit()


def main(filename: str, encode: bool, algo:str =None):
    if not algo:
        print("no regocnizable algorithm entered")
    
    with open(filename, "r") as file:
        data = file.read()

    if algo == 'huffman':
        chosen_alorithm = Huffman()

    ret = chosen_alorithm.encode(data)
    print(ret)

def generate_test_data(magnitude_of_bytes):
    random_letters = "".join(random.choices(ascii_letters, k=10**magnitude_of_bytes))
    print(random_letters)


if __name__ == "__main__":
    implemented_algorithms = ['huffman']
    # n = 1000000
    encode = True
    if "-h" in sys.argv or "help" in sys.argv:
        output_help()
    if "-g" in sys.argv:
        magnitude_of_bytes = int(sys.argv[sys.argv.index("-g") + 1])
        generate_test_data(magnitude_of_bytes)
        exit()
    if "-d" in sys.argv:
        encode = False
    if "algorithm" in sys.argv:
        algo = (sys.argv[sys.argv.index("algorithm") + 1])
        if algo not in implemented_algorithms:
            print("Currently only the following compression algorithms are available")
            for algo in implemented_algorithms:
                print(" - " + algo)
            exit()
    
    filename = sys.argv[-1]
    
    main(filename, encode, algo)