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
    '''

    def __add_nodes(self, nodes):
        node_counts = Counter(nodes)

        # Check if it's better to 
        # as_nodes = [Node(value, name) for value,name in node_count.items()]
        # self.__heap = heapq.heapify(as_nodes)

        for name, value in node_counts.items():
            heapq.heappush(self.__heap, Node(value, name))

    def __create_tree(self):
        while len(self.__heap) != 1:
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

            # otherwise add the parent node back to heap
            heapq.heappush(self.__heap, new_node)

    @classmethod
    def __create_codes(cls, node, codes:dict):

        if node.is_leaf:
            codes[node.name] = bitarray(node.bits)
            return

        node.right.bits = node.bits + "1"
        node.left.bits = node.bits + "0"

        cls.__create_codes(node.right, codes)
        cls.__create_codes(node.left, codes)

    def encode(self, iterable):
        self.__heap = []
        codes = {}
        encoded_tree = bitarray()
        encoded_content = bitarray()

        self.__add_nodes(iterable)
        root = self.__create_tree()
        self.__create_codes(root, codes)

        self.__encodeNode(root, encoded_tree)

        for symbol in iterable:
            encoded_content.extend(codes[symbol])


        print(encoded_tree)
        return encoded_tree.extend(encoded_content)

    def decode(self, encodedbits):
        raise NotImplementedError

    def __encodeNode(self, node:Node, encoded_tree):
        # Encoding huffman tree is based on 
        # https://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree
        print(encoded_tree)

        if node.is_leaf:
            encoded_tree.extend('1')
            encoded_tree.extend(format(b, '08b') for b in node.name.encode('utf-8'))
        else:
            encoded_tree.extend('0')
            self.__encodeNode(node.left, encoded_tree)
            self.__encodeNode(node.right, encoded_tree)


if __name__ == "__main__":
    test_string = "A"

    huffman = Huffman()
    encoded_bin = huffman.encode(test_string)

