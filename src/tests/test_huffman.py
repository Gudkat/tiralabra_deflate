import unittest
from bitarray import bitarray
from algorithms.huffman import *
from os import remove

HEADERSIZE = 16

class TestHuffmanCoding(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_binary_file = "test.bin"
        cls.test_string = "this is a test string"
        
    def setUp(self):
        self.huffman = Huffman()

    def tearDown(self):
        try:
            remove(self.test_binary_file)
        except:
            pass

    def test_encoding_empty_input(self):
        self.huffman.encode('', self.test_binary_file)

        with open(self.test_binary_file, "rb") as file:
            binary = bitarray()
            binary.fromfile(file)

        self.assertEqual(len(binary), HEADERSIZE, "Empty encoding should only contain header information")
        

    def test_decoding_only_header(self):
        with open(self.test_binary_file, "wb") as file:
            bitarray('0' * HEADERSIZE).tofile(file)

        decoded = self.huffman.decode(self.test_binary_file)
    
        self.assertEqual(len(decoded), 0, "Decoding binary with only header information did not yield empty string")

    def test_decoding(self):
        self.huffman.encode(self.test_string, self.test_binary_file)
        decoded = self.huffman.decode(self.test_binary_file)
        
        self.assertEqual(decoded, self.test_string, "Decoded string does not match the original.")

    def test_file_handling(self):
        self.huffman.encode(self.test_string, self.test_binary_file)        
        encoded_bits = self.huffman.filehandler.load_binary_file(self.test_binary_file)
        
        self.assertIsInstance(encoded_bits, bitarray, "Loaded binary is not of type 'bitarray'.")
        self.assertGreater(len(encoded_bits), HEADERSIZE, "Loaded binary only has 16 bits (HEADER).")

    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            self.huffman.decode("fictional.bin")
    
    def test_empty_input_E2E(self):
        empty_string = ""
        self.huffman.encode(empty_string, self.test_binary_file)
        decoded = self.huffman.decode(self.test_binary_file)
        
        self.assertEqual(decoded, empty_string, "Decoded string for empty input is not empty.")

    # def test_single_char_input_E2E(self):
    #     single_char_string = "aaaaaaa"
    #     self.huffman.encode(single_char_string, self.test_binary_file)
    #     decoded = self.huffman.decode(self.test_binary_file)
        
    #     self.assertEqual(decoded, single_char_string, "Decoded string for single character input is incorrect.")
    
    def test_large_input_E2E(self):
        with open("../testdata/bible.txt") as f:
            large_string = f.read()
        
        self.huffman.encode(large_string, self.test_binary_file)
        decoded = self.huffman.decode(self.test_binary_file)
        
        self.assertEqual(large_string, decoded, "End-to-end testing for large text file did not work")


'''
TODO: 
    * Change test data for more sensible data
    * Write tests for testing compression rate after comparable compression rates for some test data
    * After deciding final form of encoding:
        * Write test for huffmantree stucture
            * test for finding large numbre of differenty symbols
            * test for making sure that tree structure is identical when encoding and decoding
        * Write test for encoding dictionary 
    * Uncomment test for single character when the program can handle single characters
'''

if __name__ == '__main__':
    unittest.main()
