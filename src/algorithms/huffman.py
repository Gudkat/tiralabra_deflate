import heapq
from collections import Counter
from bitarray import bitarray


class Node:
    def __init__(self, value, node_name, bits="", left=None, right=None):
        self.bits = bits
        self.value = value
        self.left = left
        self.right = right
        self.name = node_name

    # Comparision required for heap.
    # If same freq, we go based on alphabets
    # Might be better to make secondary ordering based on how many chars in name
    # And tertiary comparision based on alphabets to create more balanced huffman tree
    def __lt__(self, other):
        return (self.value, self.name) < (other.value, other.name)

    @property
    def is_leaf(self):
        return not(self.left or self.right)
    
    def __str__(self):
        # for debugging. Delete later
        return f"name: {self.name}, value: {self.value}"


class Huffman:
    '''
    Encodes huffman coding for iterable input. encode method accepts iterables and returns a tuple; first item encoded bits and 2nd item encoding "table"
    TODO: 
    * Include the codes for the binary encodings
    * decode method missing
    * Tree encoding fails if only 1 kind of symbol in input
    '''

    def __iterable_to_heap(self, iterable):
        node_counts = Counter(iterable)
        nodes  = [Node(value, name) for name, value in node_counts.items()]
        heapq.heapify(nodes)

        return nodes

        # Above is probably O(n) and below is O(n log n)
        # for name, value in node_counts.items():
        #     heapq.heappush(heap, Node(value, name))

    def __create_tree(self, heap: list):
        while len(heap) > 1:
            # Take 2 lowest frequency items from heap and merge them to parent node in tree until only root remains
            right, left = heapq.heappop(heap), heapq.heappop(heap)
            new_node = Node(
                value=left.value + right.value,
                node_name=right.name + left.name,
                right=right,
                left=left,
            )
            heapq.heappush(heap, new_node)

        return heap[0]

    @classmethod
    def __create_codes(cls, node, codes:dict):

        if node.is_leaf:
            codes[node.name] = bitarray(node.bits)
            return

        node.right.bits = node.bits + "1"
        node.left.bits = node.bits + "0"

        cls.__create_codes(node.right, codes)
        cls.__create_codes(node.left, codes)

    def encode(self, iterable, filename):
        '''
        Encoding format is: 
            First 2 bytes is for the size of huffmantree in bytes
            The following is the huffmantree. 
                The encoding of the huffmantree has 2 bits for every symbol denoting how many bytes is used for the symbol.
                00 for 1 byte, 01 for 2 bytes, 10 for 3 bytes and 11 for 4 bytes
            Encoded content
        '''
        codes = {}
        compression = bitarray()
        huffman_in_bits = bitarray()
        content_in_bits = bitarray()

        heap = self.__iterable_to_heap(iterable)
        huffman_root = self.__create_tree(heap)

        self.__create_codes(huffman_root, codes)
        self.__encodeNode(huffman_root, huffman_in_bits)

        # fill method padds the bytes with zeros. 
        # We need this so that the size of the huffmantree section can be separated from the compressed content
        # alternatively calculate required filler bits... extend((8 - (len(huffman_in_bits) % 8) * '0')
        huffman_in_bits.fill()

        # +7 so that the floor division for 8 emulates ceil division. 
        # There exists method in the bitarray for this but I'm not sure 
        # how widely I shold use premade libraries

        size_of_huffman_tree_int = (len(huffman_in_bits) + 7) // 8

        # restrict to 2 bytes. 
        # TODO: Change the size denomination to dynamic size instead of fixed 2 bytes
        if size_of_huffman_tree_int > (1 << 16) -1:
            raise ValueError(f'Compression doesnt work with this many symbols.')

        how_much_space_for_huffmantree = bitarray(f'{size_of_huffman_tree_int:016b}')
        
        self.__encode_content(iterable, codes, content_in_bits)
        content_in_bits.fill()

        compression.extend(how_much_space_for_huffmantree)
        compression.extend(huffman_in_bits)
        compression.extend(content_in_bits)

        self.__save_binary_file(filename, compression)

    def decode(self, filename):
        '''
        Decodes huffman encoding in the format specified in encode method.

        Example of huffman tree encoding (010001100001100011000100):
            0 -not a leaf
            1 - leaf
            00 - 1 byte symbol
            01100001 - utf-8 encoding of symbol a
            1 - leaf
            00 - 1 byte symbol
            01100010 - utf-8 encoding of symbol b
            0 - padding
        '''

        encoded_bits = self.__load_binary_file(filename)
        print("entire encoded binary", encoded_bits.to01())

        '''

        '''

        size_of_huffman_tree = int(encoded_bits[:16].to01(), 2) * 8
        print("size_of_huffman_tree in bits", size_of_huffman_tree)

        huffman_tree_bits = encoded_bits[16:16+size_of_huffman_tree]
        content_bits = encoded_bits[16+size_of_huffman_tree:]
    
        #print huffmanbits as 1's and 0's
        print("tree bits", huffman_tree_bits.to01())

        pointer = 0
        self.__decodeNode(huffman_tree_bits, pointer, size_of_huffman_tree)

            

        print("content bits", content_bits.to01())

    def __encode_content(self, iterable, codes:dict, content_in_bits:bitarray):
        for symbol in iterable:
            print("symbol", symbol, "code", codes[symbol].to01())
            content_in_bits.extend(codes[symbol])

    def __encodeNode(self, node:Node, encoded_tree):
        # Encoding huffman tree is based on 
        # https://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree
        
        if node.is_leaf:
            encoded_tree.extend('1')
            utf8_bytes = node.name.encode('utf-8')

            # We know that we require at minimum 1 byte and at maximum 4 bytes in utf-8
            # if we use the actual number for how many bytes are required, 
            # we need 3 bits to represent number 4 (100) but we never need 0 bytes, so we can use -1 here.
            # For example, when utf-8 encoding needs 1 byte, we write byte length 00.

            how_many_bytes_in_utf8 = f'{len(utf8_bytes)-1:02b}'

            encoded_tree.extend(how_many_bytes_in_utf8)
            encoded_tree.frombytes(utf8_bytes)            
        else:
            encoded_tree.extend('0')
            self.__encodeNode(node.left, encoded_tree)
            self.__encodeNode(node.right, encoded_tree)

    def __decodeNode(self, bin: bitarray, pointer: int, size_of_huffman_tree):
        while pointer < size_of_huffman_tree:
            if bin[pointer]:
                # this is a leaf

                #move pointer to read the length of the symbol
                pointer += 1


                how_many_bytes_for_symbol = int(bin[pointer:pointer+2].to01()) + 1
                how_many_bits_for_symbol = how_many_bytes_for_symbol * 8

                # move pointer to read the actual symbol
                pointer += 2
                
                print(bin[pointer:pointer+how_many_bits_for_symbol].tobytes().decode('utf-8'))

                exit()
            else:
                # this is not a leaf
                print(True)

            pointer += 1

    @classmethod
    def __save_binary_file(cls, filename, bits:bitarray):
        with open(filename, 'wb') as file:
            bits.tofile(file)

    @classmethod
    def __load_binary_file(cls, filename):
        with open(filename, 'rb') as file:
            bits = bitarray()
            bits.fromfile(file)
        return bits

if __name__ == "__main__":

    if False:
        with open("../../testdata/bible.txt") as f:
            test_string = f.read()
        huffman = Huffman()
        encoded_bin = huffman.encode(test_string)
        print(len(test_string), len(encoded_bin) >> 3)

    huffman = Huffman()
    encoded = huffman.encode("abaa", "test.bin")
    huffman.decode("test.bin")