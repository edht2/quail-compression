
class QuailCompression:
    
    # ENCODING

    def encode(s:str) -> list:
        """ Encode the string into a Huffman binary tree and encoded bit string
        parameters:
         s : str # The string to be encoded
        returns: 
         bit_tree : str # The serialized Huffman tree
         bit_str : str # The encoded string
        """
        
        tuple_tree = QuailCompression.build_tuple_tree(s)
        
        # Serialize the tuple tree      
        bin_tree = QuailCompression.serialize_tree(tuple_tree)
        
        # Map addresses to a dictionary for faster encoding
        addr_map = QuailCompression.character_map(tuple_tree)
        char_map = {v: k for k, v in addr_map.items()}
        
        # Encode the message
        final = ""
        for char in s:
            final += char_map[char]
        
        return bin_tree, final
    
    def build_tuple_tree(s:str) -> tuple:
        """ Creates a Huffman tree of tuples from the input string """
        
        # Frequency order
        char_freq = [(c, s.count(c)) for c in list(set(s))]
        char_freq = QuailCompression.sort_freq(char_freq)
        
        # Build the tree
        tuple_tree = char_freq
        while len(tuple_tree) > 1:
            new_node = ((tuple_tree[0], tuple_tree[1]), tuple_tree[0][1] + tuple_tree[1][1])
            tuple_tree.pop(0)
            tuple_tree.pop(0)
            tuple_tree.append(new_node)
            tuple_tree = QuailCompression.sort_freq(tuple_tree)
            
        return tuple_tree[0]

    def sort_freq(f:list[tuple[str, int]]) -> list[tuple[str, int]]:
        """ Implementation of a bubble sort to allow to sort by a specific part of a list element. """
        swaps = 1
        while swaps > 0:
            swaps = 0
            for i in range(len(f)-1):
                if f[i][1] > f[i+1][1]:
                    f[i], f[i+1] = f[i+1], f[i]
                    swaps += 1
        return f
    
    def serialize_tree(node):
        """ Turn a tuple node into a binary string. This function is used recursively """
        data, freq = node
        
        if isinstance(data, str):
            char_bits = f"{ord(data):08b}"
            return "0" + char_bits
        else:
            left_child, right_child = data
            return "1" + QuailCompression.serialize_tree(left_child) + QuailCompression.serialize_tree(right_child)
    
    def character_map(decoded_node:str, current_address:str="", result_dict=None):
        """ Turns a decoded tuple tree into a dictionary of form {addr:char} this can be used to speed up encoding and decoding """
        if isinstance(decoded_node, tuple): node = decoded_node[0]
        else: node = decoded_node
        if result_dict is None:
            result_dict = {}
        if isinstance(node, str):
            result_dict[current_address] = node
        else:
            left_child, right_child = node
            QuailCompression.character_map(left_child, current_address + "0", result_dict)
            QuailCompression.character_map(right_child, current_address + "1", result_dict)

        return result_dict
    
    # DECODING
        
    def decode_serialized(bit_iterator):
        """ Turn serialised Huffman tree into a tree of tuples """
        bit = next(bit_iterator)
        if bit == '0':
            char_bits = "".join([next(bit_iterator) for _ in range(8)])
            return chr(int(char_bits, 2))
        else:
            left = QuailCompression.decode_serialized(bit_iterator)
            right = QuailCompression.decode_serialized(bit_iterator)
            return (left, right)

    def decode(bit_tree:str, bit_str:str) -> str:
        """ Decodes the string with the serialized Huffman tree
        parameters:
         bit_tree : str # The serialized Huffman tree
         bit_str : str # The encoded string
        returns: 
         s : str # The decoded string
        """
        decoded_tree = QuailCompression.decode_serialized(iter(bit_tree))
        
        decoded = ""
        cursor = decoded_tree
        
        for bit in bit_str:
            if isinstance(cursor[int(bit)], str):
                decoded += cursor[int(bit)]
                cursor = decoded_tree
            else:
                cursor = cursor[int(bit)]
        return decoded
    

