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

    def __lt__(self, other):
        return (self.value, self.name) < (other.value, other.name)

    def __str__(self):
        # for debugging. Delete later
        return f"name: {self.name}, value: {self.value}"


class Huffman:
    '''
    Encodes huffman coding for iterable input. encode method accepts iterables and returns a tuple; first item encoded bits and 2nd item encoding "table"
    TODO: 
    * Include the codes for the binary encodings
    * Something needs to be done for LZ77 backreference encoding
    * decode method missing
    '''

    def __add_nodes(self, nodes):
        node_counts = Counter(nodes)
        for name, value in node_counts.items():
            heapq.heappush(self.__heap, Node(value, name))

    def __create_tree(self):
        while True:
            right, left = heapq.heappop(self.__heap), heapq.heappop(self.__heap)
            new_node = Node(
                value=left.value + right.value,
                node_name=right.name + left.name,
                right=right,
                left=left,
            )

            # return root of huffman tree if the tree is complete
            if not self.__heap:
                return new_node

            # otherwise add the new node back to heap
            heapq.heappush(self.__heap, new_node)

    @classmethod
    def __create_codes(cls, node, codes):

        if not node.left and not node.right:
            codes[node.name] = bitarray(node.bits)
            return

        node.right.bits = node.bits + "1"
        node.left.bits = node.bits + "0"

        cls.__create_codes(node.right, codes)
        cls.__create_codes(node.left, codes)

    def encode(self, iterable):
        self.__heap = []
        codes = {}

        self.__add_nodes(iterable)
        root = self.__create_tree()
        self.__create_codes(root, codes)

        encoded_bits = bitarray()
        for sym in iterable:
            encoded_bits.extend(codes[sym])

        # Figure out how to include the codes in the encoded part
        return encoded_bits, codes

    def decode(self, encodedbits):
        raise NotImplementedError


if __name__ == "__main__":
    test_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    huffman = Huffman()
    encoded_bits, codes = huffman.encode(test_string)

    print(encoded_bits)
    print(codes)
