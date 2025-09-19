import heapq
from collections import Counter
from bitarray import bitarray

class NoBitsToDecode(Exception):
    pass

class EmptyStringEncoding(Exception):
    pass

class Node:
    def __init__(self, value, node_name, bits="", left=None, right=None):
        self.bits = bits
        self.value = value
        self.left = left
        self.right = right
        self.name = node_name

        # TODO: Clean up structure of nodes. Does the tree still need values? 
        # Does it make sense to even save bits of the node instead of traversing 
        # the tree every time

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


class BitReader:
    def __init__(self, binary:bitarray):
        self.binary = binary

        if len(self.binary) <= 16:
            raise NoBitsToDecode

        self.huffman_size = self.__get_huffman_size()
        self.filler_bits = self.__get_number_of_filler_bits()
        self.pointer = 16 # Position at the start of huffman tree in binary
    
    def __get_huffman_size(self):
        return int(self.binary[:13].to01(), 2)

    def __get_number_of_filler_bits(self):
        # This is filler bits at the end of the content encoding. Filler bits 
        # after huffman tree don't affect us due to how the recursion works.
        return int(self.binary[13:16].to01(), 2)

    def __get_length_of_next_symbol(self):
        how_many_bytes_for_symbol = int(self.binary[self.pointer:self.pointer+2].to01()) + 1
        self.pointer += 2
        return how_many_bytes_for_symbol
    
    def read_next_node(self) -> bytes:
        num_of_bytes = self.__get_length_of_next_symbol()
        symbol_bytes = self.binary[self.pointer:self.pointer+num_of_bytes*8].tobytes()
        self.pointer += num_of_bytes * 8
        return symbol_bytes
    
    @property
    def next_node_is_leaf(self):
        bit_value = self.binary[self.pointer]
        self.pointer += 1
        return bit_value
    
    def move_to_encoded_section(self):
        self.pointer = 16 + (self.huffman_size * 8)

    def bit_generator(self):
        while self.pointer < len(self.binary) - self.filler_bits:
            yield self.binary[self.pointer]
            self.pointer += 1


class BitWriter:
    header_size = 16
    def __init__(self):
        self.__binary = bitarray(16)
  
    def set_huffman_size_bits(self, bits):
        self.__binary[0:13] = bitarray(bits)

    def __set_padding_bits(self, bits):
        self.__binary[13:16] = bitarray(bits)

    def extend(self, bits):
        self.__binary.extend(bits)

    def add_padding(self):
        '''
        adds padding to fit byte frames and adds information to header section for padding size
        '''
        size_of_padding = self.__binary.fill()
        self.__set_padding_bits(f'{size_of_padding:03b}')

    def frombytes(self, bytes):
        self.__binary.frombytes(bytes)

    @property
    def binary(self):
        return self.__binary.copy()


class FileHandler:
    def save_binary_file(self, filename, bits):
        with open(filename, 'wb') as file:
            bits.tofile(file)

    def load_binary_file(self, filename):
        with open(filename, 'rb') as file:
            bits = bitarray()
            bits.fromfile(file)
        return bits


class HuffmanEncoder:
    def __init__(self, iterable:str):
        if len(iterable) == 0:
            raise EmptyStringEncoding
        
        self.iterable = iterable
        self.bit_writer = BitWriter()
        self.huffman_size = 0

    def encode(self) -> bitarray:
        self.codes = {}

        heap = self.__iterable_to_heap(self.iterable)
        huffman_root = self.__create_tree(heap)
        self.__create_codes(huffman_root)

        huffman_bits = self.__encode_huffman_tree(huffman_root)
        self.__set_huffman_tree_size_bits(huffman_bits)

        self.bit_writer.extend(huffman_bits)
        self.__encode_content(self.iterable)
        self.bit_writer.add_padding()

        return self.bit_writer.binary

    def __set_huffman_tree_size_bits(self, huffman_in_bits):
        # +7 so that the floor division for 8 emulates ceil division. 
        size_of_huffman_tree_int = (len(huffman_in_bits) + 7) // 8

        # restrict to 13 bits so that entire header is 2 bytes. 
        # TODO: Change the size denomination to dynamic size instead of fixed size
        if size_of_huffman_tree_int > (1 << 13) -1:
            raise ValueError(f'Compression doesnt work with this many symbols.')

        return self.bit_writer.set_huffman_size_bits(f'{size_of_huffman_tree_int:013b}')

    def __encode_huffman_tree(self, huffman_root) -> bitarray:
        huffman_in_bits = bitarray()

        self.__encodeNode(huffman_root, huffman_in_bits)

        # fill method padds the bytes with zeros. 
        # We need this so that the size of the huffmantree section can be separated from the compressed content
        # alternatively calculate required filler bits... extend((8 - (len(huffman_in_bits) % 8) * '0')
        huffman_in_bits.fill()

        return huffman_in_bits
        

    def __iterable_to_heap(self, iterable):
        node_counts = Counter(iterable)
        nodes  = [Node(value, name) for name, value in node_counts.items()]
        heapq.heapify(nodes)

        return nodes

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
    
    def __create_codes(self, node):
        if node.is_leaf:
            self.codes[node.name] = bitarray(node.bits)
            return

        node.right.bits = node.bits + "1"
        node.left.bits = node.bits + "0"

        self.__create_codes(node.right)
        self.__create_codes(node.left)

    def __encodeNode(self, node:Node, encoded_tree:bitarray):
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

    def __encode_content(self, iterable):
        for symbol in iterable:
            self.bit_writer.extend(self.codes[symbol])


class HuffmanDeocoder:
    def __init__(self, binary):
        self.bit_reader = BitReader(binary)
        self.huffman_root = self.__get_huffman_root()

    def __get_huffman_root(self):
        return self.__decodeNode()

    def __decodeNode(self):
        if self.bit_reader.next_node_is_leaf:
            node_name_in_bytes = self.bit_reader.read_next_node()
            node_name = node_name_in_bytes.decode('utf-8')
            return Node(value=0, node_name=node_name)
        else:
            left, right = self.__decodeNode(), self.__decodeNode()
            # TODO: place holder value and name. They are not really needed. Need to clean up Node class
            return Node(value=0, node_name='', left=left, right=right)
        
    def decode(self):
        '''
        Decodes huffman encoding in the format specified in encode method.

        Example of huffman tree encoding (010001100decoder001100011000100):
            0 -not a leaf
            1 - leaf
            00 - 1 byte symbol
            01100001 - utf-8 encoding of symbol a
            1 - leaf
            00 - 1 byte symbol
            01100010 - utf-8 encoding of symbol b
            0 - padding
        '''
        self.bit_reader.move_to_encoded_section()
        current_node = self.huffman_root
        bit_generator = self.bit_reader.bit_generator()

        # Might be a good idea to change this to write letters straight to file one by one
        # instead or storing to string. No reason to use extra space for it in case you 
        # would want to compress large files (since we are using generator for this ready).
        # Unless of course that would slow down the program. Don't think so though...

        decoded = ""

        for bit in bit_generator:
            if bit == 0:
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.is_leaf:
                decoded += current_node.name
                current_node = self.huffman_root

        return decoded
    

class Huffman:
    '''
    Encodes huffman coding for iterable input. encode method accepts iterables and returns a tuple; first item encoded bits and 2nd item encoding "table"
    TODO: 
    * Tree encoding fails if only 1 kind of symbol in input
    * Modify to iterate bytes instead of text
    '''

    def __init__(self):
        self.filehandler = FileHandler()

    def encode(self, iterable, filename):
        '''
        Encoding format is: 
            First 13 bits are for the size of huffmantree in bytes
            Next 3 bits are for number of filler bits at the end of encoding
            The following is the huffmantree. 
                The encoding of the huffmantree has 2 bits for every symbol denoting how many bytes is used for the symbol.
                00 for 1 byte, 01 for 2 bytes, 10 for 3 bytes and 11 for 4 bytes
            Encoded content
        '''
        try:
            binary  = HuffmanEncoder(iterable).encode()
        except EmptyStringEncoding:
            binary = BitWriter().binary

        self.filehandler.save_binary_file(filename, binary)

    def decode(self, filename):
        encoded_bits = self.filehandler.load_binary_file(filename)

        try:
            return HuffmanDeocoder(encoded_bits).decode()
        except NoBitsToDecode:
            return ''
        

if __name__ == "__main__":
    with open("testdata/bible.txt") as f:
        test_string = f.read()
    huffman = Huffman()
    huffman.encode(test_string, "test.bin")
    ret = huffman.decode("test.bin")
    # print(len(test_string), len(ret))
    print(test_string == ret)
    # print(test_string[:100])
    # print(ret[:100])
