# Project specification

This project is course work for the course [TKT20010](https://studies.helsinki.fi/kurssit/opintojakso/otm-3d27dcc5-f7b5-4eec-b5db-53217aee3918/TKT20010) (Aineopintojen harjoitustyö: Algoritmit ja tekoäly) in the University of Helsinki: 

The course is completed under the Computer Science bachelor program (TKT).

## Algorithms

This project implements deflate-algorithm using Python programming language. Further, the **deflate** is implemented with the help of **huffman** and **LZ77** algorithms (in some variations LZSS is used instead of LZ77). The data compression is lossless in every algorithm here.

Huffman algorithm is used to compress the original letters to less bits so that more commonly used letters are coded into less bits so that no letter is a prefix of another, thus you can automatically tell when a code for a letter ends without additional bits used for it.

LZ77 idea is to use a sliding window. The first part of the sliding window, which makes the vast majority of the window, is search buffer. The second part of the sliding window is look ahead buffer. The algorithm looks at the first letter of the look ahead buffer and tries to match it in the search buffer. If match is found it looks at the 2nd letter and tries to match it and so forth until the longest possible match is found. Then the algorithm marks how many steps backwards we look and how many characters the match was. Coding is done in the format `[D, L, c]` where the `D` stands for distance, ie. how many letters backwards we look. `L`stands for length, ie how many characters we copy and `c` stands for the next character. If `L > D` it means that we loop back to where D points until all of the length is used. so lets say 2 last letters in the search buffer are `he` and 6 first letters in the look ahead buffer are `heheh `, our algorithm would mark this `[2, 5, ' ']`. This compresses letters "heheh" (5 bytes in ascii) into the reference. If no previous match can be found for the look ahead search, it is marked as `[0, 0, c]`. The size of the reference depends on chosen values for our algorithm. We will choose 32KB as the size of the sliding window.

The Deflate algorithm combines these 2 algorithms. When compressing data you first go throught the data using LZ77 algorithm and get a mix of back references and literals. After this you encode this bitstream using huffman algorithm for both literals and back references. You will need to include this 

## How to use the program

Using the program will be implemented using CLI to run app.py file with flags and path to source file and a path to where the compressed file can be found. For example `python app.py -e /path_to/some_text_file.txt some_filename.deflate`

Available flags: 
* -e for encode (using no flag should also do the encoding)
* -d for decode

## Programming languages

This project is implemented using **Python** programming language. 

Languages that I feel comfortable doing peer reviews with: Python, Javascript, C++. 

## Time and space complexities

Since the compression of text happens in a fixed size of a window, this part should be constant (The size of the tree grows with variety of data but not exactly due to size of data) for both time and space complexity. The creation of huffman should be linear in both complexities. Decompression should be also linear.


## Sources for project

* [Huffman coding in wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)
* [LZ77 and LZ78 wikipedia](https://en.wikipedia.org/wiki/LZ77_and_LZ78)
* [Deflate in Wikipedia](https://en.wikipedia.org/wiki/Deflate)
* [Youtube video of a lecture about deflate in the University of Victoria](https://www.youtube.com/watch?v=SJPvNi4HrWQ)

## Language choice

Everything written related to the project will be done using English.