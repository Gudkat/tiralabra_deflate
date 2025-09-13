# Project specification

This project is course work for the course [TKT20010](https://studies.helsinki.fi/kurssit/opintojakso/otm-3d27dcc5-f7b5-4eec-b5db-53217aee3918/TKT20010) (Aineopintojen harjoitustyö: Algoritmit ja tekoäly) in the University of Helsinki: 

The course is completed under the Computer Science bachelor program (TKT).

The project will be about implementing compression algorithms and comparing them with different types of data.

## Algorithms

The chosen algorithms are huffman code and LZ77 compression algorithms.

**Huffman** is used to compress the original letters to less bits so that more commonly used letters are coded into less bits so that no letter is a prefix of another, thus you can automatically tell when a code for a letter ends without additional bits used for it. This is done by creating huffman tree which is included in the compressed file.

**LZ77** idea is to use a sliding window. The first part of the sliding window, which makes the vast majority of the window, is search buffer. The second part of the sliding window is look ahead buffer. The algorithm looks at the first letter of the look ahead buffer and tries to match it in the search buffer. If match is found it looks at the 2nd letter and tries to match it and so forth until the longest possible match is found. Then the algorithm marks how many steps backwards we look and how many characters the match was. Coding is done in the format `[D, L, c]` where the `D` stands for distance, ie. how many letters backwards we look. `L`stands for length, ie how many characters we copy and `c` stands for the next character. If `L > D` it means that we loop back to where D points until all of the length is used. so lets say 2 last letters in the search buffer are `he` and 6 first letters in the look ahead buffer are `heheh `, our algorithm would mark this `[2, 5, ' ']`. 


## How to use the program

The project will be implemented using poetry for managing dependencies. 

Using the compression algorithms will be implemented using CLI to run app.py. start the app.py file using -h flag to get current instructions on operating the program;`poetry run python app.py -h`.


## Programming languages

This project is implemented using **Python** programming language. 

Languages that I feel comfortable doing peer reviews with: Python, Javascript, C++. 

## Time and space complexities

We build huffman coding by creating heap for each used symbol (character in text) and their frequency. Then we combine two lowest frequency nodes to a parent node which will be put back into the heap. Worst case (every character appears once in our source) we have to do n times heap insert and pop. This gives us O(n log n) time complexity. 

LZ77 is using a sliding window of fixed size, so while the constant time that cause will be quite large, the asymptotic time and space complexities will be O(n). 



## Sources for project

* [Huffman coding in wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)
* [LZ77 and LZ78 wikipedia](https://en.wikipedia.org/wiki/LZ77_and_LZ78)


## Choice of language

Everything written related to the project will be done using English.