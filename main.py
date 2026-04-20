class QuailCompression:
    
    backref_marker = b"\0x1F" # Unit Separator
    
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
            
        # Count leaf nodes
        leaf_nodes = f'{len(addr_map):08b}'
        
        return leaf_nodes + bin_tree + final
    
    def build_tuple_tree(s:str) -> tuple:
        """ Creates a Huffman tree of tuples from the input string """
        
        # Frequency order
        char_freq = [(c, s.count(c)) for c in sorted(list(set(s)))]
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
        
    def delim(bit_str:str) -> list[str, str]:
        """ Split the long binary string into a parts. eg Binary tree part, encoded part"""
        
        # First 8 bits are the number of leaf nodes in the tree
        leaf_nodes = int(bit_str[:8], 2)
        
        cursor = 8
        found_leaves = 0
        while cursor < len(bit_str):
            if bit_str[cursor] == "0":
                cursor += 9 # skip any characters encoded in the tree
                found_leaves += 1
                if found_leaves >= leaf_nodes: break
            else:
                cursor += 1
                
        return bit_str[8:][:cursor], bit_str[cursor:]
        

    def decode(bit_str:str) -> str:
        """ Decodes the string with the serialized Huffman tree
        parameters:
         bit_str : str # The encoded string including the serialized tree and encoded bin string
        returns: 
         s : str # The decoded string
        """
        
        serialized_tree, encoded = QuailCompression.delim(bit_str)
    
        decoded_tree = QuailCompression.decode_serialized(
            iter(
                serialized_tree # Skip first 8 bits (num nodes)
            )
        )

        decoded = ""
        cursor = decoded_tree
                
        for bit in encoded:
            if isinstance(cursor[int(bit)], str):
                decoded += cursor[int(bit)]
                cursor = decoded_tree
            else:
                cursor = cursor[int(bit)]
        return decoded
    

